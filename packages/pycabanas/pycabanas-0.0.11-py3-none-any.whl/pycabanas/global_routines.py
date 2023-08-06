import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from matplotlib import ticker
from resamplelib.jackknife import *
def ticks_format(value, index):
    """
    This function decompose value in base*10^{exp} and return a latex string.
    If 0<=value<99: return the value as it is.
    if 0.1<value<0: returns as it is rounded to the first decimal
    otherwise returns $base*10^{exp}$
    I've designed the function to be use with values for which the decomposition
    returns integers
    """
    exp = np.floor(np.log10(value))
    base = value/10**exp
    #print(value,exp,base)
    if exp == 0 or exp == 1:
        #return '${0:d}$'.format(int(value))
        return '${}$'.format(int(value))
    if exp == -1:
        return '${0:.1f}$'.format(value)
    else:
        #return '${0:d}10^{{{1:d}}}$'.format(int(base), int(exp))
        return '${}10^{}$'.format(int(base), int(exp))
####################################################################

# EQUILIBRIUM ROUTINES

####################################################################
def array_equilibrium(lista,name,plot_fig,x_label,y_label):
    res=[]
    plt.clf()
    plt.cla()
    #print(lista)
    for gg in lista:
         
         data=gg[1]
         #print(data)
         shape=np.shape(data)
         instances=shape[0]
         windows=shape[1]
         end = False
         l_fin=10
         windows_computed=0
         data_conv_array=[]
         data_conv_sigma=[]
         data_conv_len=[]
         while end==False:
              if(windows_computed<windows):
                   #Computing the average for the segment
                   data_avg=np.average(data[:,windows_computed])
                   #Computing the error for the segment
                   sigma_avg=np.sqrt(np.sum(np.power((data[:,windows_computed]-data_avg),2))/np.float64(instances*(instances-1)))
                   #Saveing the results
                   data_conv_array.append(data_avg)
                   data_conv_sigma.append(sigma_avg)
                   data_conv_len.append(l_fin)
                   windows_computed+=1
              else:
                   end=True
              #Defining the limits for the next range
              l_fin=3*l_fin
              if(windows_computed<windows):
                    #Computing the average for the segment
                   data_avg=np.average(data[:,windows_computed])
                   #Computing the error for the segment
                   sigma_avg=np.sqrt(np.sum(np.power((data[:,windows_computed]-data_avg),2))/np.float64(instances*(instances-1)))
                   #Saveing the results
                   data_conv_array.append(data_avg)
                   data_conv_sigma.append(sigma_avg)
                   data_conv_len.append(l_fin)
                   windows_computed+=1
                   #Defining the limits for the next range
                   l_fin=int(10*l_fin/3)
              else:
                   end=True
         #The last data is for the results
         res.append([gg[0],data_conv_array[-1],data_conv_sigma[-1]])
         if(plot_fig):
           try:
                
                plt.errorbar(data_conv_len,data_conv_array, yerr=data_conv_sigma, fmt='o', label=str(round(gg[0],2) ))
                #plt.plot(data_conv_len,data_conv_array, )
                
           except:
                print('Cant plot data')
    if(plot_fig):
      #plt.tight_layout()
      plt.xscale('log')
      plt.xlabel('MC steps')
      plt.ylabel(y_label)
      plt.tick_params( direction='in',bottom=True, top=True, left=True, right=True)
      plt.tick_params( which='minor',direction='in',bottom=True, top=True, left=True, right=True)
      plt.rc('font', family='serif')
      #plt.tight_layout()
      plt.rcParams.update({'font.size': 10})
      plt.rc('text', usetex=True)
      plt.legend(title=r'$\Gamma$',frameon=False,loc='best',fontsize=10)
      plt.tight_layout()
      plt.savefig('equilibrium_'+name+'.eps')
      plt.clf()
      plt.cla()
      # Plotting the results
      plt.rcParams.update({'font.size': 10})
      plt.rc('text', usetex=True)
      plt.tight_layout()
      plt.xlabel(x_label)
      plt.ylabel(y_label)
      plt.yscale('log')
      res=np.array(res)
      #print(res[0,:],type(res))
      plt.errorbar(res[:,0],res[:,1], yerr=res[:,2], fmt='+', label=None)
      plt.tight_layout()
      plt.savefig('fig_'+name+'.eps',bbox_inches="tight")
      plt.clf()
      plt.cla()
      plt.close
    return res
def sort_and_build(lista,exp):
     ##############################################################################
     #  The first column constins gamma, the others, the window equilibrium values
     #  Here I sort, for each gamma value, the window samples
     ##############################################################################
     #
     #First we get the gamma values of the firs column:
     gamma=np.unique(lista[:,0])
     #print(gamma)
     data=[]
     for g in gamma:
         #Getting the 
         aux=np.power(lista[np.where(lista[:,0]== g)],exp)
         data.append([g,  aux[:,1:] ])
     return data

def plot_histogram_q(data,arr):
     def funci(x):
      return x
     windows=np.unique(data[:,0])
     gamma=np.unique(data[:,1])
     x_values=np.unique(data[:,2])
     f=open('q_aver.dat','w')
     for w in windows:
         clean1=data[np.where(data[:,0]==w)]
         plt.clf()
         plt.cla()
         plt.rcParams.update({'font.size': 10})
         plt.rc('text', usetex=True)
         plt.tight_layout()
         plt.ylabel(r'$P(q)$')
         plt.xlabel(r'$Q$')
         #plt.ylim((0,2.5))
         #print(res[0,:],type(res))
         for g in gamma:
            clean2=clean1[np.where(clean1[:,1]==g)]
            x_array=[]
            y_array=[]
            err_array=[]
            for x in x_values:
                clean3=clean2[np.where(clean2[:,2]==x)]
                #print(clean3)
                # Select normalized histogram values
                y=clean3[:,3]
                #print(y)
                # average histogram values
                y_aver,y_err,*rest=jackknife_1d(y,funci)
                x_array.append(x)
                y_array.append(y_aver)
                err_array.append(y_err)
                # For the last window we print the results to file
                if (w==windows[-1]):
                    f.write(str(g)+'\t'+str(x)+'\t'+str(y_aver)+'\t'+str(y_err)+'\n')
            #Plotting the averaged histogram
            if ((g in arr) or (len(arr)==0)):
                plt.errorbar(x_array,y_array, yerr=err_array, fmt='+', label=str(g))
         plt.legend(loc='upper left')
         plt.tight_layout()
         plt.savefig('histogram_q_window'+str(w)+'.eps')
         plt.clf()
         plt.cla()
     plt.close
     f.close()
def plot_histogram_q_l(data,arr):
     def funci(x):
      return x
     windows=np.unique(data[:,0])
     gamma=np.unique(data[:,1])
     x_values=np.unique(data[:,2])
     f=open('q_l_aver.dat','w')
     for w in windows:
         clean1=data[np.where(data[:,0]==w)]
         plt.clf()
         plt.cla()
         plt.rcParams.update({'font.size': 10})
         plt.rc('text', usetex=True)
         plt.tight_layout()
         plt.ylabel(r'$P(q)$')
         plt.xlabel(r'$Q$')
         #plt.ylim((0,2.5))
         #print(res[0,:],type(res))
         for g in gamma:
            clean2=clean1[np.where(clean1[:,1]==g)]
            x_array=[]
            y_array=[]
            err_array=[]
            for x in x_values:
                clean3=clean2[np.where(clean2[:,2]==x)]
                #print(clean3)
                # Select normalized histogram values
                y=clean3[:,3]
                #print(y)
                # average histogram values
                y_aver,y_err,*rest=jackknife_1d(y,funci)
                x_array.append(x)
                y_array.append(y_aver)
                err_array.append(y_err)
                # For the last window we print the results to file
                if (w==windows[-1]):
                    f.write(str(g)+'\t'+str(x)+'\t'+str(y_aver)+'\t'+str(y_err)+'\n')
            #Plotting the averaged histogram
            if ((g in arr) or (len(arr)==0)):
                plt.errorbar(x_array,y_array, yerr=err_array, fmt='+', label=str(g))
         plt.legend(loc='upper left')
         plt.tight_layout()
         plt.savefig('histogram_q_l_window'+str(w)+'.eps')
         plt.clf()
         plt.cla()
     plt.close
     f.close()
####################################################################

# CORRELATION ROUTINES

####################################################################
def compute_correlation_from_MC(correlation):#,observable):
    #Getting gammas and t
    delta=np.unique(correlation[:,1])
    gamma=np.unique(correlation[:,0])
    results=open('w_correlation.dat','a')
    for g in gamma:
        #Computing the Jack-Knife of the average
        #obs_MC=np.power(observable[np.where(observable[:,0]== g)],1)
        #obs_jk_2=jack_knife(obs_MC[:,1],2)
        #Getting the data of t
        aux=np.power(correlation[np.where(correlation[:,0]== g)],1)
        #record=[]
        for t in delta:
            aux1=np.power(aux[np.where(aux[:,1]== t)],1)
            #corr_jk_1=jack_knife(aux1[:,2], 1)
            #print(corr_jk_1,obs_jk_2)
            #corrA=corr_jk_1-obs_jk_2
            corrA=jackknife_2d(aux1[:,2],aux1[:,3],correlation_imtime)
            results.write(str(g)+"\t"+str(t)+"\t"+str(corrA[0])+"\t"+str(corrA[1])+"\n")
            #record.append(corrA)
        #results.write(str(g)+"\t"+str('  '.join(map(str,record)))+"\n")
    return
def compute_correlation_from_disorder(correlation):
    gamma=np.unique(correlation[:,0])
    delta=np.unique(correlation[:,1])
    print(gamma)
    count=0
    energies=[]
    plt.rc('font', family='serif')
    plt.rcParams.update({'font.size': 17})
    plt.rc('text', usetex=True)

    for g in gamma:
      aux=np.power(correlation[np.where(correlation[:,0]== g)],1)
      res=[]
      
      #
      #for t in delta:
      #  aux1=np.power(aux[np.where(aux[:,1]== t)],1)
      #  print(aux1)
      #  aux2=binning(aux1[:,2])
      #  res.append([t,aux2[0],aux2[1]])
      fit=True
      if fit:
        fit_params=[
        [15,30], #2.5
        [15,30], #2.58
        [15,30], #2.66
        [15,30], #2.75
        [15,30], #2.83
        [15,30], #2.91
        [15,30], #3.0
        [15,30], #3.08       
        [15,30], #3.16
        [15,30], #3.25
        [15,30], #3.33
        [15,30], #3.41
        [15,30], #3.5
        [15,30], #3.58
        [15,30], #3.66
        [15,25], #3.75
        [15,30], #3.83
        [15,24], #3.91
        [12,25], #4.0
        [12,25], #4.08       
        [12,23], #4.16
        [12,17], #4.25
        [10,19], #4.33
        [10,17], #4.41
        [10,15]] #4.5
        #Compute de the fit and gap
        print('plotting',g)
        y=aux[:,2]
        x=aux[:,1]
        #c,e_fit=fitting1(x[fit_params[count][0]:fit_params[count][1]],y[fit_params[count][0]:fit_params[count][1]])
        plt.errorbar(aux[:,1],aux[:,2] ,yerr=aux[:,3] ,fmt='+',label=r'$C(\tau)$')
        try:
          c,e_fit,e_err=fitting1(x[fit_params[count][0]:fit_params[count][1]],y[fit_params[count][0]:fit_params[count][1]])
          energies.append([g,e_fit,e_err])
          plt.plot(x,func(np.asarray(x),c,e_fit),'-',label="fit")
          
       	except:
       		print('not fitted')
        e_err=round_sig(e_err)
        e_fit=round_to_reference(e_fit, e_err)
        plt.xlim((0,30))
        plt.ylim((10**(-4),1))
        plt.yscale('log')
        plt.xlabel(r'$\tau$')
        plt.ylabel(r'$C(\tau)$')
        plt.figtext(0.2,0.30,r'$\Gamma = {}$'.format(round(g,2)))
        plt.figtext(0.2,0.25,r'$\Delta E_1 = {} \pm {}$'.format(e_fit,e_err))
        plt.figtext(0.2,0.20,r'Fit range  {} to {}'.format(fit_params[count][0],fit_params[count][1]))
        plt.tick_params( direction='in',bottom=True, top=True, left=True, right=True)
        plt.tick_params( which='minor',direction='in',bottom=True, top=True, left=True, right=True)
        plt.rc('font', family='serif')
        plt.tight_layout()
        plt.rcParams.update({'font.size': 17})
        plt.rc('text', usetex=True)
        plt.legend(frameon=False,loc='best',fontsize=12)
        ax = plt.axes()
        ax.yaxis.set_major_formatter(ticker.NullFormatter())
        ax.yaxis.set_major_formatter(ticker.FuncFormatter(ticks_format))
        ax.yaxis.set_minor_formatter(ticker.NullFormatter())
        plt.savefig(str(g)+'_gap.eps')
        plt.clf()
        plt.cla()
        count+=1
      else:
        print(count,count % 5)
        if ((count % 5)==0):
          res=np.array(res)
          plt.errorbar(aux[:,1],aux[:,2] ,yerr=aux[:,3] ,fmt='+',label=str(round(g,2)))
        count+=1
            #brake
    plt.xlim((0,30))
    plt.ylim((10**(-4),1.))
    plt.yscale('log')
    plt.xlabel(r'$\tau$')
    plt.ylabel(r'$C(\tau)$')
    plt.tight_layout()
    plt.tick_params( direction='in',bottom=True, top=True, left=True, right=True)
    plt.tick_params( which='minor',direction='in',bottom=True, top=True, left=True, right=True)
    plt.rc('font', family='serif')
    plt.rcParams.update({'font.size': 17})
    plt.rc('text', usetex=True)
    plt.legend(title=r'$L$',frameon=False,loc='best',fontsize=12)
    ax = plt.axes()
    ax.yaxis.set_major_formatter(ticker.NullFormatter())
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(ticks_format))
    ax.yaxis.set_minor_formatter(ticker.NullFormatter())
    plt.rc('font', family='serif')
    plt.rcParams.update({'font.size': 15})
    plt.rc('text', usetex=True)
    print('help')
    plt.savefig('multiple_gamma_gap.eps')
    print('help1')
    plt.clf()
    plt.cla()
    #Plotting energy profile
    energies=np.array(energies)
    plt.errorbar(energies[:,0],energies[:,1] ,yerr=energies[:,2] ,fmt='+',label=r'$\Delta E_1$')
    #plt.yscale('log')
    plt.legend(loc='best')
    plt.xlabel(r'$\Gamma$')
    plt.ylabel(r'$\Delta E$')
    plt.ylim((0,0.5))
    plt.tick_params( direction='in',bottom=True, top=True, left=True, right=True)
    plt.tick_params( which='minor',direction='in',bottom=True, top=True, left=True, right=True)
    plt.rc('font', family='serif')
    plt.tight_layout()
    plt.rcParams.update({'font.size': 17})
    plt.rc('text', usetex=True)
    plt.legend(frameon=False,loc=(0.2,0.8),fontsize=15)
    plt.savefig('energy_gap_profile.eps')
    plt.close()
def correlation_imtime(xx,x2):
	return xx-x2**2.
def compute_gap_derivate(y):
    gap=[]
    for i in range(1,len(y)-1):
        gap.append(-(y[i+1]-y[i-1])/(2.*y[i]))
    e=np.average(gap[30:])
    return gap,e
def fitting1(x,y):
	x=np.asarray(x)
	y=np.asarray(y)
	print(x)
	print(y)
	popt, pcov = curve_fit(func, x, y)
	#Error
	print(popt)
	perr=np.sqrt(np.diag(pcov))
	
	#print(perr)
	#print("Parameters",popt)
	c_fit,e_fit = popt
	c_err,e_err = perr
	return c_fit,e_fit
def func(x,c,e):
	res=c*np.exp(-e*x)
	return res