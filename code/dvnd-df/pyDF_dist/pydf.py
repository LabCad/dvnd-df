# Python Dataflow Library
# Tiago A.O.Alfes <tiago@ime.uerj.br>

from multiprocessing import Process, Queue, Value, Pipe
import threading

import sys


class Worker(Process):
	def __init__(self, graph, operand_queue, conn, workerid):
		Process.__init__(self)  # since we are overriding the superclass's init method
		# self.taskq = task_queue
		self.operq = operand_queue
		self.idle = False
		self.graph = graph
		self.wid = workerid
		self.conn = conn  # connection with the scheduler to receive tasks

	# def sendops(self, opers):
	# print "%s sending oper" %self.name
	#	self.operq.put(opers)

	def run(self):
		print "I am worker %s" % self.wid
		self.operq.put([Oper(self.wid, None, None, None)])  # Request a task to start

		while True:
			# print "Waiting for task %s" %self.name
			task = self.conn.recv()

			# print "Start working %s" %(self.name)
			node = self.graph.nodes[task.nodeid]
			node.run(task.args, self.wid, self.operq)
		# self.sendops(opermsg)


class Task:
	def __init__(self, f, nodeid, args=None):
		self.nodeid = nodeid
		self.args = args


class DFGraph:
	def __init__(self):
		self.nodes = []
		self.node_count = 0

	def add(self, node):
		node.id = self.node_count
		self.node_count += 1

		self.nodes += [node]


class Node:
	def __init__(self, f, inputn):
		self.f = f
		self.inport = [[] for i in range(inputn)]
		self.dsts = []
		self.affinity = None

	def add_edge(self, dst, dstport):
		self.dsts += [(dst.id, dstport)]

	def pin(self, workerid):
		self.affinity = workerid

	def run(self, args, workerid, operq):
		# print "Running %s" %self
		if len(self.inport) == 0:
			opers = self.create_oper(self.f(), workerid, operq)
		else:
			opers = self.create_oper(self.f([a.val for a in args]), workerid, operq)
		self.sendops(opers, operq)

	def sendops(self, opers, operq):
		operq.put(opers)

	def create_oper(self, value, workerid, operq):  # create operand message
		opers = []
		if self.dsts == []:
			opers.append(Oper(workerid, None, None,
				None))  # if no output is produced by the node, we still have to send a msg to the scheduler.
		else:
			for (dstid, dstport) in self.dsts:
				oper = Oper(workerid, dstid, dstport, value)
				opers.append(oper)
			# print "Result produced %s (worker: %d)" %(oper.val, workerid)
		return opers

	def match(self):
		args = []
		for port in self.inport:
			if len(port) > 0:
				arg = port[0]
				args += [port[0]]
		if len(args) == len(self.inport):
			for inport in self.inport:
				arg = inport[0]
				inport.remove(arg)
			return args
		else:
			return None


class Oper:
	def __init__(self, prodid, dstid, dstport, val):
		self.wid, self.dstid, self.dstport, self.val = prodid, dstid, dstport, val
		# wid -> id of the worker that produced the oper
		# dstid -> id of the target task
		# dstport -> input port of the target task
		# val -> actual value of the operand

		self.request_task = True  # if true, piggybacks a request for a task to the worker where the opers were produced.


class Scheduler:
	TASK_TAG = 0
	OPER_TAG = 1
	TERMINATE_TAG = 2

	def __init__(self, graph, n_workers=1, mpi_enabled=True):
		# self.taskq = Queue()  #queue where the ready tasks are inserted
		self.operq = Queue()

		self.graph = graph
		self.tasks = []
		worker_conns = []
		self.conn = []
		self.waiting = []  # queue containing idle workers
		self.n_workers = n_workers  # number of workers
		self.pending_tasks = [0] * n_workers  # keeps track of the number of tasks sent to each worker without a request from the worker (due to affinity)
		for i in range(n_workers):
			sched_conn, worker_conn = Pipe()
			worker_conns += [worker_conn]
			self.conn += [sched_conn]
		self.workers = [Worker(self.graph, self.operq, worker_conns[i], i) for i in range(n_workers)]

		if mpi_enabled:
			self.mpi_handle()
		else:
			self.mpi_rank = None

	def mpi_handle(self):
		from mpi4py import MPI
		comm = MPI.COMM_WORLD
		rank = comm.Get_rank()
		self.mpi_size = comm.Get_size()
		self.mpi_rank = rank
		self.n_slaves = self.mpi_size - 1
		self.keep_working = True

		print "There are %s mpi processes. (hostname = %s)" % (self.mpi_size, MPI.Get_processor_name())
		self.pending_tasks = [0] * self.n_workers * self.mpi_size
		self.mpi_outq = Queue()
		# self.mpi_inq = Queue()

		status = MPI.Status()

		def mpi_input(inqueue):
			while self.keep_working:
				msg = comm.recv(source=MPI.ANY_SOURCE, tag=MPI.ANY_TAG, status=status)
				# print "MPI Received opermsg from slave."
				if status.Get_tag() == Scheduler.TASK_TAG:
					# send task
					task = msg
					connid = task.workerid % self.n_workers
					self.conn[connid].send(task)
				elif status.Get_tag() == Scheduler.OPER_TAG:
					# receive oper
					if self.mpi_rank > 0:
						msg.request_task = False  # only the leader receives task requests through mpi
					inqueue.put([msg])
				elif status.Get_tag() == Scheduler.TERMINATE_TAG and self.mpi_rank > 0:
					self.keep_working = False
					print "Got termination tag %d" % self.mpi_rank
					self.terminate_workers(self.workers)

			print "Saindo thread in rank %d" % (self.mpi_rank)

		def mpi_output(outqueue):
			while self.keep_working:
				print "Waiting outqueue %d" % self.mpi_rank
				msg = outqueue.get()
				print "Received outqueue %d %s" % (self.mpi_rank, msg)

				if msg != None:  # msg == None means termination
					# print "MPI Sending task to slave node."
					if isinstance(msg, Task):
						task = msg
						dest = task.workerid / self.n_workers  # destination mpi process
						comm.send(task, dest=dest, tag=Scheduler.TASK_TAG)
					else:
						oper = msg
						wid = oper.wid
						if oper.dstid == None:
							dest = 0
						else:
							dst = self.graph.nodes[oper.dstid]
							if dst.affinity == None or oper.val == None:
								dest = 0
							else:
								dest = dst.affinity[0] / self.n_workers
						comm.send(oper, dest=dest, tag=Scheduler.OPER_TAG)
				else:
					mpi_terminate()
			print "Saindo thread out rank %d" % (self.mpi_rank)

		def mpi_terminate():
			print "MPI TERMINATING (rank = %d)" % self.mpi_rank
			self.keep_working = False
			if self.mpi_rank == 0:
				for i in xrange(0, self.mpi_size):
					comm.send(None, dest=i, tag=Scheduler.TERMINATE_TAG)

			print "FINISHED MPI TERMINATING (rank = %d)" % self.mpi_rank

		t_in = threading.Thread(target=mpi_input, args=(self.operq,))
		t_out = threading.Thread(target=mpi_output, args=(self.mpi_outq,))

		threads = [t_in, t_out]
		self.threads = threads
		for t in threads:
			t.start()

	def propagate_op(self, oper):
		dst = self.graph.nodes[oper.dstid]
		if self.mpi_rank is not None:
			if dst.affinity is not None and (dst.affinity[0] / self.n_workers) == self.mpi_rank \
					or dst.affinity is None and self.mpi_rank == 0:
				# TODO Comentada mensagem
				# print "Propagating Internally %s (rank %s)" % (oper.val, self.mpi_rank)
				self.internal_opsnd(oper)
			else:
				# TODO Comentada mensagem
				# print "Propagating Externally %s (rank %s)" % (oper.val, self.mpi_rank)
				self.mpi_outq.put(oper)
		else:
			self.internal_opsnd(oper)

	def internal_opsnd(self, oper):
		dst = self.graph.nodes[oper.dstid]
		dst.inport[oper.dstport] += [oper]
		args = dst.match()

		if args is not None:
			self.issue(dst, args)

	def check_affinity(self, node):
		if node.affinity is None:
			return None

		affinity = node.affinity[0]
		if len(node.affinity) > 1:
			node.affinity = node.affinity[1:] + [node.affinity[0]]
		return affinity

	def check_task_affinity(self, task):
		node = self.graph.nodes[task.nodeid]

		return self.check_affinity(node)

	def issue(self, node, args):

		#	print "Args %s " %args
		task = Task(node.f, node.id, args)
		self.tasks += [task]

	def all_idle(self):
		# print [(w.idle, w.name) for w in workers]
		# print "All idle? %s (rank %d)" %(reduce(lambda a, b: a and b, [w.idle for w in self.workers]), self.mpi_rank)
		if self.mpi_rank == 0:
			return len(self.waiting) == self.n_workers * self.mpi_size
		else:
			print "Idles are %s (rank %d) %s" % (self.waiting, self.mpi_rank, len(self.waiting) == self.n_workers)
			return len(self.waiting) == self.n_workers

	def terminate_workers(self, workers):
		print "Terminating workers %s %d %d (rank = %d)" % (
		self.all_idle(), self.operq.qsize(), len(self.tasks), self.mpi_rank)
		# if self.mpi_rank == 0:
		finish_oper = Oper(0, None, None, None)
		finish_oper.request_task = False  # oper created to bump the scheduler out of the blocking operq.get() after termination
		self.operq.put([finish_oper])

		self.mpi_outq.put(None)
		for worker in workers:
			worker.terminate()

	def request_task(self, workerid):
		self.mpi_outq.put(Oper(workerid, None, None, None))  # Request a task to the leader

	def start(self):
		operq = self.operq

		print "Roots %s" % [r for r in self.graph.nodes if len(r.inport) == 0]
		if self.mpi_rank == 0:
			for root in [r for r in self.graph.nodes if len(r.inport) == 0]:
				task = Task(root.f, root.id)
				self.tasks += [task]

		if self.mpi_rank > 0:
			for worker in self.workers:
				worker.wid += self.mpi_rank * self.n_workers
		for worker in self.workers:
			print "Starting %s" % worker.wid
			worker.start()

		# if self.mpi_rank == 0 or self.mpi_rank == None:
		# it this is the leader process or if mpi is not being used
		print "Main loop"
		self.main_loop()
		print "Fim main loop rank %d" % self.mpi_rank
		for t in self.threads:
			print "Joining %s (rank %d)" % (t, self.mpi_rank)
			t.join()
			print "Joinied %s (rank %d)" % (t, self.mpi_rank)

	def main_loop(self):
		tasks = self.tasks
		operq = self.operq
		workers = self.workers
		while len(tasks) > 0 or not self.all_idle() or operq.qsize() > 0 or (self.mpi_rank > 0 and self.keep_working):
			# TODO Comentando mensagem de debug
			# print "Test %d %s" % (self.mpi_rank, self.keep_working)
			opersmsg = operq.get()
			for oper in opersmsg:
				if oper.val != None:
					self.propagate_op(oper)

			wid = opersmsg[0].wid
			if wid not in self.waiting and opersmsg[0].request_task:
				if self.pending_tasks[wid] > 0:
					self.pending_tasks[wid] -= 1
				else:
					self.waiting += [wid]  # indicate that the worker is idle, waiting for a task
				if self.mpi_rank is not None and self.mpi_rank > 0 and len(tasks) == 0:
					self.request_task(wid)  # request task to the leader

			while len(tasks) > 0 and len(self.waiting) > 0:
				task = tasks.pop(0)
				wid = self.check_task_affinity(task)
				if wid is not None:
					if wid in self.waiting:
						self.waiting.remove(wid)
					else:
						self.pending_tasks[wid] += 1  # send to destination
				else:
					wid = self.waiting.pop(0)
				# print "Got opermsg from worker %d" %wid
				if self.mpi_rank is None or (wid / self.n_workers == self.mpi_rank):  # local worker
					if self.mpi_rank is not None:
						wid = wid % self.n_workers
					worker = workers[wid]

					self.conn[wid].send(task)
				else:
					task.workerid = wid
					self.mpi_outq.put(task)
		# TODO Comentando mensagem de debug
		# print "Waiting %s (end of mail loop)" % self.waiting
		if self.mpi_rank == 0 or self.mpi_rank is None:
			self.terminate_workers(self.workers)
