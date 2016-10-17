
# coding: utf-8

# In[53]:

get_ipython().magic(u'pylab inline')


# In[54]:

import math
import numpy as np
import pylab as plt
from scipy.special import gamma
import scipy.integrate as spint
import xraylib


# In[55]:

def func1(E):
    """
    This function calculate an intrinsic part of the spectrum.
    
    :param l: wavelength
    :type l: int, float
    :returns: an array of intensity values
    :rtype: float
    """
    b=1.0 # константа, узнается из эксперимента
    z=29.0 # порядковый номер элемента анода(медь)
    v=40.0 # напряжение на в трубке
    Ek=v #критическая(максимальная) энергия
    res = b*z*v*v/12.39/12.39*E*E*(Ek/12.39-1/12.39*E)
    return res


# In[56]:

def func2(E):
    """
    This function calculate an intrinsic part of the spectrum.
    
    :param l: wavelength
    :type l: int, float
    :returns: an array of intensity values
    :rtype: float
    """
    b=1.0 # константа, узнается из эксперимента
    z=29.0 # порядковый номер элемента анода(медь)
    v=40.0 # напряжение на в трубке
    Ek=v #критическая(максимальная) энергия
    res = b*z*v*v/12.39/12.39*E*E*E*(Ek/12.39-1/12.39*E)
    return res


# In[57]:

v = 40 # напряжение на в трубке
Ek=v #критическая(максимальная) энергия
E=np.arange(0, Ek, 0.1) # массив длинн волн


# In[58]:

def absorb(intensity, E, material, s): #поглощение
    """
    This function calculate the intensity of the radiation given absorption 0.5mm cuprum.
    
    :param l: wavelength
    :param intensity: intensity without absorption
    :param material: absorbing layer
    :param s: the thickness of the absorbing layer
    :returns: intensity with absorption
    :rtype: float
    """
    r = 5.32873
    c = 3.0
    h = 6.62
    e = E
    A=[]
    for ae in e:
        A.append(exp(-xraylib.CS_Total_CP(material, ae)*r*s))
    return intensity*A


# In[59]:

def absorb2(E): #поглощение
    """
    This function calculate the intensity of the radiation given absorption 0.5mm cuprum.
    
    :param l: wavelength
    :param intensity: intensity without absorption
    :param material: absorbing layer
    :param s: the thickness of the absorbing layer
    :returns: intensity with absorption
    :rtype: float
    """
    r = 5.32873
    c = 3.0
    h = 6.62
    e = E
    material = 'H2O'
    s = 0.01
    res2 = func1(E)*exp(-xraylib.CS_Total_CP(material, E)*r*s)
    return res2


# In[60]:

intensity = func1(E) # полный спектр


# In[61]:

plt.figure(figsize=(10,5))
plt.plot(E,intensity, label='Spectr')
plt.plot(E,absorb(intensity, E, 'H2O', 0.01), label='Absorption spectrum')
plt.grid(True)
plt.legend(loc=0)
plt.title('Spectr')
plt.xlabel('Energy(KeV)')
plt.ylabel('Intensity')


# In[62]:

# рассчет контрастности полихроматического пучка
Ekr = np.arange(10, 40, 1)
free, _ = spint.quad(func,0,Ek) # интенсивность без поглащения
absorbs, _ = spint.quad(absorb2,0,Ek) # интенсивность c поглащением
print (free-absorbs)/free


# In[63]:

# график зависимомти <E>(Ekr)
Eeff = []
Et = []
for ae in Ekr:
    temp1, _ = spint.quad(func2,0,ae)
    temp2, _ = spint.quad(func1,0,ae)
    Eeff.append(temp1/temp2) # усредненная энергия
    Et.append(0.66*ae) 
plt.figure(figsize=(10,5))
plt.plot(Ekr,Eeff, label='Calc')
plt.plot(Ekr, Et, label='Teor')
plt.grid(True)
plt.legend(loc=0)
plt.title('Spectr')
plt.xlabel('Critical energy')
plt.ylabel('Effective energy')


# In[49]:

ae = 0
while ae < 30:
    print (ae, Eeff[ae], Ekr[ae], Eeff[ae]/Ekr[ae])
    ae = ae + 1


# In[ ]:



