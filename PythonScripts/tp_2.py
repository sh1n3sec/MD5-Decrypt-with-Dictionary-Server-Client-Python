import os, hashlib, threading, time, itertools, multiprocessing, signal
from multiprocessing import Queue
pipe_name ='/home/so/so_server'
pipe_dec ='/home/so/so_2'

#Project Made By Pedro Gomes 2017/2018
""" THREAD DE PESQUISA """

def threads_pesquisa(q, content, ev, inicio, fim, qt):
	
	while True:
		if ev.is_set() == True:

			encrypt_pass = q.get()
			arr = []
						
			for x in range (inicio, fim):
			
				#word = "test"
				#for x in map(''.join, itertools.product(*zip(word.upper(), word.lower()))):
										
				arr = map (''.join, itertools.product(*zip(content[x].upper(), content[x].lower())))

				code = hashlib.md5(arrpalavra.encode()).hexdigest()

				#code = hashlib.md5(content[x].encode()).hexdigest()
				
				if code == encrypt_pass:
					pass_dec = content[x]
					print ("Palava encontrada: "+pass_dec)					
					qt.put(pass_dec)
					ev.clear()					
					
""" THREAD DE CONTROLO """
	
def thread_controlo(q1, q2, ev, qt):
	
	while True:
		pipein = open(pipe_dec)
		encrypt_pass = pipein.readline()[:-1] 
		pipein.close()
		
		print ("Recebida " +encrypt_pass)
		q1.put(encrypt_pass)
		q2.put(encrypt_pass)	
		ev.set()
		
		while True:
			try:	
				pass_found = qt.get(timeout=1)
			
			except Exception:
				pass_found = None
					
			if pass_found:				
				break


		pipeout = open(pipe_name, 'w')
		pipeout.write('grupo_2 : '+pass_found+' : '+encrypt_pass+'\n')
		pipeout.close()
		ev.set()

""" FUNÇÃO DE COMEÇO """	

def encrypt():	
	
	content = []
	with open('/home/so/dicionario.txt') as f:
		content = f.readlines()		
		content = [x.strip() for x in content]
	f.close()


	ev = threading.Event()
	
	q1 = Queue()
	q2 = Queue()
	qt = Queue()
	
	p1 = threading.Thread(name="threads_pesquisa_1", target=threads_pesquisa, args=(q1, content, ev, 0, 1200, qt))
	p2 = threading.Thread(name="threads_pesquisa_2", target=threads_pesquisa, args=(q2, content, ev, 1200, 2400, qt))	
	t = threading.Thread(name="thread_controlo", target=thread_controlo, args=(q1, q2, ev, qt))
	
	p1.start()	
	p2.start()
	t.start()
		
	p1.join()
	p2.join()
	t.join()

""" SINAL PARA PEDIR CONTAGEM (Ctrl+Z) """

"""
def z_contar(signum, frame):
	signal.signal(signal.SIGINT, signal.SIG_IGN)
	log('Signal handler called with signal '+str(signum))
	time.sleep(5)
	signal.signal(signal.SIGINT, handler)
	log("signal end!")
"""

""" SINAL PARA SAIR (Ctrl+C) """

def c_sair():
	print("A terminar...")
	exit()

""" MAIN """

if not os.path.exists(pipe_dec):
	os.mkfifo(pipe_dec)

""" CONFIGURAR OS SINAIS """

# Ctrl+Z
#signal.signal(signal.SIGINT, z_contar)
# Ctrl+C
signal.signal(signal.SIGTSTP, c_sair)

encrypt()
