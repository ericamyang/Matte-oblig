import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
#løser varmelikningen i 2D numerisk med eksplisitt metode
lengde = 1 #lengde av flaten
bredde = 1 #bredden av flaten
a = 0.1 #varmedifusivitets konstatn
tid = 10 #sekunder

punkter = 15
tid_punkter = 10000 

dx = lengde/(punkter-1) #steg lengde i x-position
dy = bredde/(punkter-1) #steg lengde i y-position
dt = tid/(tid_punkter-1) #steg lengde i tid

u = np.zeros((punkter, punkter, tid_punkter)) #matrise for varmefordelingen over flaten

x = np.linspace(0, lengde, punkter) #de diskrete x-verdiene 
y = np.linspace(0, bredde, punkter) #de diskrete y-verdiene

#Initialkrav
#u(x, y, 0) = f(x, y) = sin(pi*x) + sin(pi*y)
for i in range (1, punkter-1):
    for j in range (1, punkter-1):
        u[i, j, 0] = np.sin(np.pi*x[i]) + 5*np.sin(np.pi*y[i])

#Randkrav
#u(0, 0, t) = u(0, bredde, t) = u(lengde, 0, t) = u(lengde, bredde, t) = 0
u[0, :, :] = u[-1, :, :] = u[:, 0, :] = u[:, -1, :] = 0

#Eksplisitt metode 
for k in range (tid_punkter-1):
    for i in range (1, punkter-1):
        for j in range (1, punkter-1):
            u[i, j, k+1] = u[i,j,k] + a*(dt/dx**2) * (u[i+1, j, k] - 2 * u[i, j, k] + u[i-1, j, k]) + a*(dt/dy**2) * (u[i, j+1, k] - 2 * u[i, j, k] + u[i, j-1, k])

#plotting
fig, axis = plt.subplots()
tidstekst = axis.text(0.02, 0.95, '', transform = axis.transAxes)

def init():
    global coloraxis
    coloraxis = axis.imshow(u[:, :, 0], extent = (0, lengde, 0, bredde), origin = 'lower', vmin = np.min(u), vmax = np.max(u))
    fig.colorbar(coloraxis)
    return coloraxis, tidstekst

def update(frame):
    coloraxis.set_data(u[:, :, frame])
    tidstekst.set_text('Tid: {:.2f}s'.format(frame*dt))
    return coloraxis, tidstekst

ani = animation.FuncAnimation(fig, update, frames = tid_punkter, init_func = init, blit=False, interval = 50)
plt.title("Varmelikningen")
plt.xlabel("X")
plt.ylabel("Y")
plt.show()

