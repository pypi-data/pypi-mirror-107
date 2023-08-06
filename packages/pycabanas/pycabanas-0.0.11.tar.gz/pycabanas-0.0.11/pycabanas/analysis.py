from pycabanas.global_routines import *
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
from resamplelib.jackknife import *
def classic_analysis(suceptibility,binder,correlation,L,rho,arr_q=[],arr_ql=[]):
	def compute_cumulants_gammas(q2,q4,sp):
		q2_l=sort_and_build(q2,1)
		q4_l=sort_and_build(q4,1)
		sp_l=sort_and_build(sp,1)

		res=[]
		for i,j,k in zip(q2_l,q4_l,sp_l):
			su=jackknife_1d(np.array(i[1][:,-1]),suceptibility)
			bi=jackknife_2d(np.array(i[1][:,-1]),np.array(j[1][:,-1]),binder)
			xi=jackknife_2d(np.array(i[1][:,-1]),np.array(k[1][:,-1]),correlation)
			res.append([i[0],su[0],su[1],bi[0],bi[1],xi[0],xi[1]])
		res=np.array(res)
		#
		plt.rcParams.update({'font.size': 10})
		plt.rc('text', usetex=True)
		plt.tight_layout()
		plt.xlabel(r'$T$')
		plt.ylabel(r'$\chi / L^{\rho-1}$')
		plt.yscale('log')
		plt.errorbar(res[:,0],res[:,1], yerr=res[:,2], fmt='+', label=None)
		plt.tight_layout()
		plt.savefig('fig_susceptibility.eps')
		plt.clf()
		plt.cla()
		#
		plt.rcParams.update({'font.size': 10})
		plt.rc('text', usetex=True)
		plt.tight_layout()
		plt.xlabel(r'$T$')
		plt.ylabel(r'$g$')
		plt.errorbar(res[:,0],res[:,3], yerr=res[:,4], fmt='+', label=None)
		plt.tight_layout()
		plt.savefig('fig_binder.eps')
		plt.clf()
		plt.cla()
		#
		plt.rcParams.update({'font.size': 10})
		plt.rc('text', usetex=True)
		plt.tight_layout()
		plt.xlabel(r'$T$')
		plt.ylabel(r'$\xi/L$')
		plt.yscale('log')
		plt.errorbar(res[:,0],res[:,5], yerr=res[:,6], fmt='+', label=None)
		plt.tight_layout()
		plt.savefig('fig_xi_L.eps')
		plt.clf()
		plt.cla()
		plt.close

		return res

	#energy=np.loadtxt('window_energy.dat' )
	q=np.loadtxt('window_q.dat')
	q2=np.loadtxt('window_q2.dat')
	q4=np.loadtxt('window_q4.dat')
	sp=np.loadtxt('window_sp.dat')
	n_instances=np.shape(q)

	#Computing equilibriums
	q=array_equilibrium(sort_and_build(q,1),'q', True,r'$T$',r'$q$')
	q2_avg=array_equilibrium(sort_and_build(q2,1),'q2', True,r'$T$',r'$q^2$')
	q4_avg=array_equilibrium(sort_and_build(q4,1),'q4', True,r'$T$',r'$q^4$')
	sp_avg=array_equilibrium(sort_and_build(sp,1),'sp', True,r'$T$',r'$S(p)$')
	#Computing cumulants
	cumulants=compute_cumulants_gammas(q2,q4,sp)
	#Printing FSS file
	number=np.shape(q2_avg)[0]
	fcc=open('fss.dat','w')
	fcc.write('# Number of instances :'+str(n_instances[0]/number)+'\n')
	for j in cumulants:
		#print(j)
		fcc.write(str(j[0])+'\t'+str(L)+'\t'+str(j[1])+'\t'+str(j[2])+'\t'+str(j[3])+'\t'+str(j[4])+'\t'+str(j[5])+'\t'+str(j[6])+'\n')
	fcc.close()
	# Computing histograms
	try:
		histogram_q=np.loadtxt('histogram_q.dat')
		histogram_q_l=np.loadtxt('histogram_q_l.dat')
		print('overlap histograms')
		plot_histogram_q(histogram_q,arr_q)
		print('link histograms')
		plot_histogram_q_l(histogram_q_l,arr_ql)
	except:
		print('No histograms')
	return
def quantum_analysis(suceptibility,binder,correlation,L,rho,arr_q=[],arr_ql=[]):
	def compute_cumulants_gammas(q2,q4,sp):
		q2_l=sort_and_build(q2,1)
		q4_l=sort_and_build(q4,1)
		sp_l=sort_and_build(sp,1)

		res=[]
		for i,j,k in zip(q2_l,q4_l,sp_l):
			su=jackknife_1d(np.array(i[1][:,-1]),suceptibility)
			bi=jackknife_2d(np.array(i[1][:,-1]),np.array(j[1][:,-1]),binder)
			xi=jackknife_2d(np.array(i[1][:,-1]),np.array(k[1][:,-1]),correlation)
			res.append([i[0],su[0],su[1],bi[0],bi[1],xi[0],xi[1]])
		res=np.array(res)
		#
		plt.rcParams.update({'font.size': 17})
		plt.rc('text', usetex=True)
		plt.tight_layout()
		plt.xlabel(r'$T\Gamma$')
		plt.ylabel(r'$\chi / L^{\rho-1}$')
		plt.yscale('log')
		plt.errorbar(res[:,0],res[:,1], yerr=res[:,2], fmt='+', label=None)
		plt.tight_layout()
		plt.savefig('fig_susceptibility.eps')
		plt.clf()
		plt.cla()
		#
		plt.rcParams.update({'font.size': 17})
		plt.rc('text', usetex=True)
		plt.tight_layout()
		plt.xlabel(r'$\Gamma$')
		plt.ylabel(r'$g$')
		plt.errorbar(res[:,0],res[:,3], yerr=res[:,4], fmt='+', label=None)
		plt.tight_layout()
		plt.savefig('fig_binder.eps')
		plt.clf()
		plt.cla()
		#
		plt.rcParams.update({'font.size': 17})
		plt.rc('text', usetex=True)
		plt.tight_layout()
		plt.xlabel(r'$\Gamma$')
		plt.ylabel(r'$\xi/L$')
		plt.yscale('log')
		plt.errorbar(res[:,0],res[:,5], yerr=res[:,6], fmt='+', label=None)
		plt.tight_layout()
		plt.savefig('fig_xi_L.eps')
		plt.clf()
		plt.cla()
		plt.close

		return res

	#energy=np.loadtxt('window_energy.dat' )
	q=np.loadtxt('window_q.dat')
	q2=np.loadtxt('window_q2.dat')
	q4=np.loadtxt('window_q4.dat')
	sp=np.loadtxt('window_sp.dat')
	n_instances=np.shape(q)

	#Computing equilibriums
	q=array_equilibrium(sort_and_build(q,1),'q', True,r'$\Gamma$',r'$q$')
	q2_avg=array_equilibrium(sort_and_build(q2,1),'q2', True,r'$\Gamma$',r'$q^2$')
	q4_avg=array_equilibrium(sort_and_build(q4,1),'q4', True,r'$\Gamma$',r'$q^4$')
	sp_avg=array_equilibrium(sort_and_build(sp,1),'sp', True,r'$\Gamma$',r'$S(p)$')
	#Computing cumulants
	cumulants=compute_cumulants_gammas(q2,q4,sp)
	#Printing FSS file
	number=np.shape(q2_avg)[0]
	fss=open('fss.dat','w')
	fss.write('# Number of instances :'+str(n_instances[0]/number)+'\n')
	for j in cumulants:
		#print(j)
		fss.write(str(j[0])+'\t'+str(L)+'\t'+str(j[1])+'\t'+str(j[2])+'\t'+str(j[3])+'\t'+str(j[4])+'\t'+str(j[5])+'\t'+str(j[6])+'\n')
	fss.close()
	# Computing histograms
	try:
		histogram_q=np.loadtxt('histogram_q.dat')
		histogram_q_l=np.loadtxt('histogram_q_l.dat')
		plot_histogram_q(histogram_q,arr_q)
		plot_histogram_q_l(histogram_q_l,arr_ql)
	except:
		print('No histograms')
	return