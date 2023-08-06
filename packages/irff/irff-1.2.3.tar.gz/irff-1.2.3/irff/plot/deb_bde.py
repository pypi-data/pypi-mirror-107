from ase.io.trajectory import TrajectoryWriter,Trajectory
from irff.AtomDance import AtomDance
from ase.calculators.singlepoint import SinglePointCalculator
from ase.io import read,write
from ase import units
from ase.visualize import view
from irff.irff_np import IRFF_NP
# from irff.tools import deb_energy
import matplotlib.pyplot as plt
from irff.AtomDance import AtomDance
import numpy as np


def plot(e,Eb,Eu,Eo,El,Ea,Et,Ep,Etor,Ef,Ev,show=False):
    plt.figure(figsize=(15,20))    
    plt.subplot(4,3,1)   
    plt.plot(Eb,alpha=0.8,linestyle='-',color='b',label='Ebond')
    plt.legend(loc='best',edgecolor='yellowgreen')

    plt.subplot(4,3,2)   
    plt.plot(Eo,alpha=0.8,linestyle='-',color='b',label='Eover')
    plt.legend(loc='best',edgecolor='yellowgreen')

    plt.subplot(4,3,3)   
    plt.plot(Eu,alpha=0.8,linestyle='-',color='b',label='Eunder')
    plt.legend(loc='best',edgecolor='yellowgreen')

    plt.subplot(4,3,4)   
    plt.plot(Ea,alpha=0.8,linestyle='-',color='b',label='Eang')
    plt.legend(loc='best',edgecolor='yellowgreen')

    plt.subplot(4,3,5)   
    plt.plot(Et,alpha=0.8,linestyle='-',color='b',label='Etcon')
    plt.legend(loc='best',edgecolor='yellowgreen')

    plt.subplot(4,3,6)   
    plt.plot(Ep,alpha=0.8,linestyle='-',color='b',label='Epen')
    plt.legend(loc='best',edgecolor='yellowgreen')

    plt.subplot(4,3,7)   
    plt.plot(El,alpha=0.8,linestyle='-',color='b',label='Elone')
    plt.legend(loc='best',edgecolor='yellowgreen')
    
    plt.subplot(4,3,8)   
    plt.plot(Et,alpha=0.8,linestyle='-',color='b',label='Etor')
    plt.legend(loc='best',edgecolor='yellowgreen')
    
    plt.subplot(4,3,9)   
    plt.plot(Ef,alpha=0.8,linestyle='-',color='b',label='Efcon')
    plt.legend(loc='best',edgecolor='yellowgreen')
    
    plt.subplot(4,3,10)   
    plt.plot(Ev,alpha=0.8,linestyle='-',color='b',label='Evdw')
    plt.legend(loc='best',edgecolor='yellowgreen')
    
    Ebv = np.array(Ev) + np.array(Eb) + np.array(Eo) + np.array(Eu)
    plt.subplot(4,3,11)   
    plt.plot(Ebv,alpha=0.8,linestyle='-',color='b',label='Evdw+Eb+Eo+Eu')
    plt.legend(loc='best',edgecolor='yellowgreen')
    
    plt.subplot(4,3,12)   
    plt.plot(e,alpha=0.8,linestyle='-',color='b',label='Total Energy')
    plt.legend(loc='best',edgecolor='yellowgreen')
    plt.savefig('deb_energies.pdf')
    if show: plt.show()
    plt.close()

def deb_energy(images,debframe=[],i=6,j=8,show=False):
    ir = IRFF_NP(atoms=images[0],
                 libfile='ffield.json',
                 nn=True)
    ir.calculate_Delta(images[0])

    Eb,Ea,e = [],[],[]
    Eo,Ev,Eu,El = [],[],[],[]
    Etor,Ef,Ep,Et = [],[],[],[]

    for i_,atoms in enumerate(images):       
        ir.calculate(images[i_])
        # print('%d Energies: ' %i_,'%12.4f ' %ir.E, 'Ebd: %8.4f' %ir.ebond[0][1],'Ebd: %8.4f' %ir.ebond[2][3] )
        Eb.append(ir.Ebond)
        Ea.append(ir.Eang)
        Eo.append(ir.Eover)
        Ev.append(ir.Evdw)
        Eu.append(ir.Eunder)
        El.append(ir.Elone)
        Ep.append(ir.Epen)
        Et.append(ir.Etcon)
        Ef.append(ir.Efcon)
        Etor.append(ir.Etor)
        e.append(ir.E)
        
    plot(e,Eb,Eu,Eo,El,Ea,Et,Ep,Etor,Ef,Ev,show=show)
    return e


def deb_bo(images,i=0,j=1,figsize=(16,10),show=False):
    bopsi,boppi,boppp,bo0,bo1,eb = [],[],[],[],[],[]
    
    ir = IRFF_NP(atoms=images[0],
                 libfile='ffield.json',
                 nn=True)
    ir.calculate_Delta(images[0])
    
    for i_,atoms in enumerate(images):       
        ir.calculate(atoms)
        
        bopsi.append(ir.eterm1[i][j])
        boppi.append(ir.eterm2[i][j])
        boppp.append(ir.eterm3[i][j])
        bo0.append(ir.bop[i][j])      
        bo1.append(ir.bo0[i][j])  
        eb.append(ir.ebond[i][j])    
    
    emin_ = np.min(eb)
    eb = (emin_ - np.array(eb) )/emin_

    plt.figure(figsize=figsize)     
    plt.plot(bopsi,alpha=0.8,linewidth=2,linestyle=':',color='k',label=r'$BO_p^{\sigma}$')
    plt.plot(boppi,alpha=0.8,linewidth=2,linestyle='-.',color='k',label=r'$BO_p^{\pi}$')
    plt.plot(boppp,alpha=0.8,linewidth=2,linestyle='--',color='k',label=r'$BO_p^{\pi\pi}$')
    plt.plot(bo0,alpha=0.8,linewidth=2,linestyle='-',color='g',label=r'$BO^{t=0}$')
    plt.plot(bo1,alpha=0.8,linewidth=2,linestyle='-',color='y',label=r'$BO^{t=1}$')
    plt.plot(eb,alpha=0.8,linewidth=2,linestyle='-',color='r',label=r'$E_{bond}$ ($-E_{bond}/%4.2f$)' %-emin_)
    plt.legend(loc='best',edgecolor='yellowgreen')
    plt.savefig('deb_bo.pdf')
    if show: plt.show()
    plt.close()

# images = Trajectory('md.traj')
# E = []
# for atoms in images:
#     E.append(atoms.get_potential_energy())


# # In[14]:


# e = deb_energy(images)



# plt.figure()
# e_ = np.array(e) - np.min(e)
# E_ = np.array(E) - np.min(E)
# plt.plot(e_,alpha=0.8,linestyle='-',color='b',label='Total Energy')
# plt.plot(E_,alpha=0.8,linestyle='-',color='r',label='DFT Energy')
# plt.legend(loc='best',edgecolor='yellowgreen')
# plt.show()

