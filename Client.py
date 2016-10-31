import sys
import socket
import select
import os

class Client:
	def __init__(self):
		self.IP='10.14.90.206'
		self.MASTER='10.14.90.206'
		self.SOCKET_LIST=[]
		self.RECV_BUFFER=4096
		self.PORT=3123
		self.CWS_PORT = 3124
		self.nw=0
		self.nr=0
		self.WRITE_Q=[]
		self.UPDATE_Q=[]
		
		try:
			self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.s.connect((self.MASTER,self.PORT))
			self.SOCKET_LIST.append(self.s)
			sys.stdout.write('Client Started\n');sys.stdout.flush()
			cws_sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
			cws_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
			cws_sock.bind((self.IP,self.CWS_PORT))
			cws_sock.listen(10)
			self.SOCKET_LIST.append(cws_sock)
		except Exception as e:
			print 'Unable to connect to ',self.MASTER
			print e
			
		while(True):
			ready_to_read,ready_to_write,in_err=select.select(self.SOCKET_LIST,[],[],0)
			for sock in ready_to_read:
				if sock == cws_sock:
					sockfd,addr=sock.accept()
					self.SOCKET_LIST.append(sockfd)
					self.ws_sock=sockfd
					sys.stdout.write('Socket connection established with '+str(addr)+'\n');sys.stdout.flush()
				
				elif sock == self.s:
					data=sock.recv(self.RECV_BUFFER)
					sys.stdout.write(data);sys.stdout.flush()
					if(data.split('#')[0]=='WRT_PERM'):
						self.unicast(self.ws_sock,data)
						self.nw=self.nw+1				
					elif(data.split('#')[0] == 'TOKEN'):
						self.unicast(sock,'LEADER_ACK#')						
						self.MASTER=self.IP						
						try:
							self.s.close()
						except Exception as e:
							sys.stdout.write('Socket connection with prev Master cannot be closed\n');sys.stdout.flush()
						self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
						self.s.connect((self.MASTER,self.PORT))
						self.SOCKET_LIST=[self.ws_sock,cws_sock]
						self.SOCKET_LIST.append(self.s)
						self.unicast(self.s,'TOKEN#')
						self.unicast(self.ws_sock,'WRT_PERM#')
						
					elif(data.split('#')[0]=='LEADER'):
						self.MASTER=data.split('#')[1]
						try:
							self.s.close()
						except Exception as e:
							sys.stdout.write('Socket connection with prev Master cannot be closed\n');sys.stdout.flush()
						self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
						self.s.connect((self.MASTER,self.PORT))
						self.SOCKET_LIST=[self.ws_sock,cws_sock]
						self.SOCKET_LIST.append(self.s)
						
					elif(data.split('#')[0]=='READ_REQ'):
						self.nr=self.nr+1						
						
					elif(data.split('#')[0]=='UPDATE'):						
						uq = data.split('#')[1]
						for q in uq:
							self.UPDATE_Q.append(q)						
											
				elif sock == self.ws_sock:
					data=self.ws_sock.recv(self.RECV_BUFFER)
					sys.stdout.write(data.split('#')[0]);sys.stdout.flush()
					if(data.split('#')[0]=='WRT_REQ'):
						self.unicast(self.s,'WRT_REQ#')						
						self.WRITE_Q.append(data.split('#')[1])
						
					elif(data.split('#')[0]=='READ_REQ'):						
						self.unicast(self.s,data)						
						msg='UPDATEDB#'
						for q in self.UPDATE_Q:
							msg=msg+q
						msg=msg+'#'
						self.unicast(self.ws_sock,msg)
						self.UPDATE_Q=[]
					elif(data.split('#')[0]=='MASTER_IP'):
						self.unicast(self.ws_sock,'IP_MASTER#'+self.MASTER+'#')
					
			if(self.nr>2 or self.nw>1):				
				updates='UPDATE#'
				for q in self.WRITE_Q:
					updates=updates+q
				updates=updates+'#'
				self.unicast(self.s,updates)	
				self.nr=0
				self.nw=0
				self.WRITE_Q=[]

	def unicast(self,sock,msg):
		try:
			sock.send(msg)
		except Exception as e:
			print 'Unable to unicast message'
			print e
		return

Client()			
