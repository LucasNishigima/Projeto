from ursina import *

app = Ursina()

# Corpo
body = Entity(model='cube', color=color.azure, scale=(1,2,0.5), position=(0,0,0))

# Cabeça
head = Entity(model='sphere', color=color.yellow, scale=0.7, position=(0,1.4,0))

# Braços
arm_left = Entity(model='cube', color=color.azure, scale=(0.3,1,0.3), position=(-0.8,0.5,0))
arm_right = Entity(model='cube', color=color.azure, scale=(0.3,1,0.3), position=(0.8,0.5,0))

# Pernas
leg_left = Entity(model='cube', color=color.brown, scale=(0.3,1,0.3), position=(-0.3,-1,0))
leg_right = Entity(model='cube', color=color.brown, scale=(0.3,1,0.3), position=(0.3,-1,0))

camera.position = (0,1.5,-5)

app.run()