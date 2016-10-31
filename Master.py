import sys
import socket
import select

class Master:
	def __init__(self):
		self.ACTIVE=True
		self.OWN_IP='10.14.90.206'
		self.SOCKET_LIST=[]
		self.ADDR_LIST=[]
		self.HAS_TOKEN=True
		self.RECV_BUFFER=4096
		self.PORT=3123
		
		client_sock_own = None
		
		try:
			self.server_socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
			self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
			self.server_socket.bind((self.OWN_IP,self.PORT))
			self.SOCKET_LIST.append(self.server_socket)
			self.server_socket.listen(10)
		except Exception as e:
			print 'Master unable to start..'
			print e
			sys.exit()
		print 'Master has started....'
		while(True):
			ready_to_read,ready_to_write,in_err=select.select(self.SOCKET_LIST,[],[],0)						
			for sock in ready_to_read:
				if(sock==self.server_socket):
					sockfd,addr=self.server_socket.accept()
					self.SOCKET_LIST.append(sockfd)
					self.ADDR_LIST.append(addr[0])
					sys.stdout.write('Socket connection established with '+str(addr)+'\n');sys.stdout.flush()
					if(sockfd.getpeername()[0] == self.OWN_IP):
						client_sock_own = sockfd			
				else:					
					data=sock.recv(self.RECV_BUFFER)		
					sys.stdout.write(data);sys.stdout.flush()									
					if data.split('#')[0]=='WRT_REQ':												
						sys.stdout.write('Write request received from '+str(sock.getpeername())+'\n');sys.stdout.flush()
						if self.check_status() and sock.getpeername()[0]==self.OWN_IP:
							self.unicast(sock,'WRT_PERM#')							
						elif self.HAS_TOKEN:
							self.HAS_TOKEN=False							
							self.unicast(sock,'TOKEN#')
							self.set_status(False)
						else:
							sys.stdout.write('Master is inactive and has no token\n');sys.stdout.flush()
							self.unicast(sock,'WRT_NOT_PERM#')
						
					elif(data.split('#')[0]=='LEADER_ACK'):
						sys.stdout.write('Leader Acknowledgement received\n');sys.stdout.flush()
						new_master=sock.getpeername()[0]
						leader_msg = 'LEADER#'+str(new_master)+'#'
						self.broadcast(sock,leader_msg)
						sys.stdout.write('Message Broadcasted '+new_master+'\n');sys.stdout.flush()						
						for s in ready_to_read:
							if(s!=self.server_socket):
								try:
									s.close()
								except Exception as e:
									sys.stdout.write('Unable to close socket\n');sys.stdout.flush()
						self.SOCKET_LIST=[]
						self.SOCKET_LIST.append(self.server_socket)
						self.ADDR_LIST=[]
						self.ADDR_LIST.append(self.OWN_IP)
					
					elif(data.split('#')[0]=='UPDATE'):
						sys.stdout.write('Update Message received\n');sys.stdout.flush()
						self.broadcast(sock,data)						
													
					elif(data.split('#')[0]=='READ_REQ'):						
						sys.stdout.write('Read Request recieved from '+str(sock.getpeername()));sys.stdout.flush()
						if(client_sock_own is not None and sock.getpeername()[0]!=self.OWN_IP):
							self.unicast(client_sock_own,'READ_REQ#')
					
					elif(data.split('#')[0]=='TOKEN'):
						if(self.check_status()):
							sys.stdout.write('Already a master ...\n');sys.stdout.flush()
						else:
							self.set_status(True)	
							self.HAS_TOKEN=True					
					else:
						continue
	
	def check_status(self):
		return self.ACTIVE
	
	def set_status(self,status):
		self.ACTIVE=status
		self.TOKEN=status
		return
	
	def unicast(self,sock,msg):
		try:
			sock.send(msg)
		except Exception as e:
			print 'Unicast failed'
			print e
		return
	
	def broadcast(self,sock,msg):	
		for s in self.SOCKET_LIST:
			if s!=self.server_socket and sock!=s:
				try:
					s.send(msg)
				except Exception as e:
					print 'Broadcast failed'
					print e
		return
					
m=Master()
		
	
	
			
		
