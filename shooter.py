import tkinter as tk
import math
import random

class DoomClone(tk.Canvas):
    def __init__(self, master):
        super().__init__(master, bg='black', highlightthickness=0)
        self.pack(fill='both', expand=True)
        
        # Game state
        self.pos_x, self.pos_y = 4.5, 4.5
        self.dir_x, self.dir_y = -1, 0
        self.plane_x, self.plane_y = 0, 0.66
        self.kills = 0
        self.health = 100
        self.enemies = []
        
        # Map configuration
        self.map_size = 8
        self.map = [
            [1,1,1,1,1,1,1,1],
            [1,0,0,0,0,0,0,1],
            [1,0,1,0,1,1,0,1],
            [1,0,0,0,0,0,0,1],
            [1,0,1,0,1,1,0,1],
            [1,0,0,0,0,0,0,1],
            [1,0,1,1,0,1,0,1],
            [1,1,1,1,1,1,1,1]
        ]
        
        # Controls
        self.move_speed = 0.2  # Increased movement speed
        self.rot_speed = 0.1
        self.keys = {
            'w': False, 's': False, 
            'a': False, 'd': False,
            'Left': False, 'Right': False
        }
        
        # Bind controls
        self.bind_all('<KeyPress>', self.key_press)
        self.bind_all('<KeyRelease>', self.key_release)
        self.bind('<Button-1>', self.shoot)
        self.focus_set()
        
        self.spawn_enemies()
        self.game_loop()

    def key_press(self, e):
        if e.keysym in self.keys:
            self.keys[e.keysym] = True
            
    def key_release(self, e):
        if e.keysym in self.keys:
            self.keys[e.keysym] = False

    def spawn_enemies(self):
        for _ in range(5):
            while True:
                x, y = random.randint(1,6), random.randint(1,6)
                if self.map[x][y] == 0:
                    self.enemies.append({
                        'x': x + 0.5,
                        'y': y + 0.5,
                        'alive': True,
                        'type': random.choice(['imp', 'zombie'])
                    })
                    break

    def move_player(self):
        # Improved movement with collision buffer
        move_speed = self.move_speed
        rot_speed = self.rot_speed
        
        # Forward/backward movement with collision prevention
        if self.keys['w']:
            new_x = self.pos_x + self.dir_x * move_speed
            new_y = self.pos_y + self.dir_y * move_speed
            if self.map[int(new_x)][int(new_y)] == 0:
                self.pos_x, self.pos_y = new_x, new_y
                
        if self.keys['s']:
            new_x = self.pos_x - self.dir_x * move_speed
            new_y = self.pos_y - self.dir_y * move_speed
            if self.map[int(new_x)][int(new_y)] == 0:
                self.pos_x, self.pos_y = new_x, new_y
                
        # Strafe left/right
        if self.keys['a']:
            new_x = self.pos_x - self.dir_y * move_speed
            new_y = self.pos_y + self.dir_x * move_speed
            if self.map[int(new_x)][int(new_y)] == 0:
                self.pos_x, self.pos_y = new_x, new_y
                
        if self.keys['d']:
            new_x = self.pos_x + self.dir_y * move_speed
            new_y = self.pos_y - self.dir_x * move_speed
            if self.map[int(new_x)][int(new_y)] == 0:
                self.pos_x, self.pos_y = new_x, new_y
        
        # Rotation
        if self.keys['Left']:
            self.rotate(rot_speed)
        if self.keys['Right']:
            self.rotate(-rot_speed)

    def rotate(self, angle):
        cos = math.cos(angle)
        sin = math.sin(angle)
        
        # Rotate direction vector
        old_dir_x = self.dir_x
        self.dir_x = old_dir_x * cos - self.dir_y * sin
        self.dir_y = old_dir_x * sin + self.dir_y * cos
        
        # Rotate camera plane
        old_plane_x = self.plane_x
        self.plane_x = old_plane_x * cos - self.plane_y * sin
        self.plane_y = old_plane_x * sin + self.plane_y * cos

    def shoot(self, e):
        # Raycast forward to check for hits
        ray_dir_x = self.dir_x
        ray_dir_y = self.dir_y
        
        map_x, map_y = int(self.pos_x), int(self.pos_y)
        delta_dist_x = abs(1 / ray_dir_x) if ray_dir_x != 0 else 1e30
        delta_dist_y = abs(1 / ray_dir_y) if ray_dir_y != 0 else 1e30
        
        step_x = 1 if ray_dir_x < 0 else -1
        side_dist_x = (self.pos_x - map_x) * delta_dist_x if ray_dir_x < 0 else (map_x + 1.0 - self.pos_x) * delta_dist_x
        step_y = 1 if ray_dir_y < 0 else -1
        side_dist_y = (self.pos_y - map_y) * delta_dist_y if ray_dir_y < 0 else (map_y + 1.0 - self.pos_y) * delta_dist_y
        
        hit = False
        while not hit:
            if side_dist_x < side_dist_y:
                side_dist_x += delta_dist_x
                map_x += step_x
                side = 0
            else:
                side_dist_y += delta_dist_y
                map_y += step_y
                side = 1
            
            if map_x < 0 or map_x >= self.map_size or map_y < 0 or map_y >= self.map_size:
                break
            
            # Check for enemies
            for enemy in self.enemies:
                if enemy['alive'] and int(enemy['x']) == map_x and int(enemy['y']) == map_y:
                    enemy['alive'] = False
                    self.kills += 1
                    return
                    
            if self.map[map_x][map_y] > 0:
                break

    def raycast(self):
        w, h = self.winfo_width(), self.winfo_height()
        
        # Cast rays for walls
        for x in range(w // 4):  # Reduced resolution
            camera_x = 2 * x / (w // 4) - 1
            ray_dir_x = self.dir_x + self.plane_x * camera_x
            ray_dir_y = self.dir_y + self.plane_y * camera_x
            
            map_x, map_y = int(self.pos_x), int(self.pos_y)
            delta_dist_x = abs(1 / ray_dir_x) if ray_dir_x != 0 else 1e30
            delta_dist_y = abs(1 / ray_dir_y) if ray_dir_y != 0 else 1e30
            
            step_x = 1 if ray_dir_x < 0 else -1
            side_dist_x = (self.pos_x - map_x) * delta_dist_x if ray_dir_x < 0 else (map_x + 1.0 - self.pos_x) * delta_dist_x
            step_y = 1 if ray_dir_y < 0 else -1
            side_dist_y = (self.pos_y - map_y) * delta_dist_y if ray_dir_y < 0 else (map_y + 1.0 - self.pos_y) * delta_dist_y
            
            hit = False
            while not hit:
                if side_dist_x < side_dist_y:
                    side_dist_x += delta_dist_x
                    map_x += step_x
                    side = 0
                else:
                    side_dist_y += delta_dist_y
                    map_y += step_y
                    side = 1
                
                if map_x < 0 or map_x >= self.map_size or map_y < 0 or map_y >= self.map_size:
                    break
                
                if self.map[map_x][map_y] > 0:
                    hit = True
            
            if hit:
                perp_wall_dist = (map_x - self.pos_x + (1 - step_x)/2) / ray_dir_x if side == 0 else (map_y - self.pos_y + (1 - step_y)/2) / ray_dir_y
                line_height = int(h / (perp_wall_dist + 0.0001))
                color = "#004400" if side == 1 else "#002200"
                self.create_line(x*4, h//2 - line_height//2, x*4, h//2 + line_height//2, fill=color, width=4)

        # Draw enemies
        for enemy in self.enemies:
            if not enemy['alive']:
                continue
                
            # Calculate enemy position relative to player
            dx = enemy['x'] - self.pos_x
            dy = enemy['y'] - self.pos_y
            
            # Transform to camera space
            inv_det = 1.0 / (self.plane_x * self.dir_y - self.dir_x * self.plane_y)
            transform_x = inv_det * (self.dir_y * dx - self.dir_x * dy)
            transform_y = inv_det * (-self.plane_y * dx + self.plane_x * dy)
            
            if transform_y > 0:  # Only draw enemies in front
                sprite_x = int((w/2) * (1 + transform_x / transform_y))
                sprite_height = int(h / transform_y)
                sprite_width = sprite_height // 2
                
                # Draw enemy
                color = "#FF0000" if enemy['type'] == 'imp' else "#00FF00"
                self.create_rectangle(
                    sprite_x - sprite_width//2, h//2 - sprite_height//2,
                    sprite_x + sprite_width//2, h//2 + sprite_height//2,
                    fill=color, outline=""
                )

    def draw_hud(self):
        w, h = self.winfo_width(), self.winfo_height()
        
        # Weapon
        self.create_line(w//2 - 20, h - 50, w//2 + 20, h - 50, fill="#00FF00", width=4)
        self.create_line(w//2, h - 70, w//2, h - 30, fill="#00FF00", width=4)
        
        # Crosshair
        self.create_line(w//2 - 15, h//2, w//2 + 15, h//2, fill="#00FF00")
        self.create_line(w//2, h//2 - 15, w//2, h//2 + 15, fill="#00FF00")
        
        # Stats
        self.create_text(20, 20, text=f"KILLS: {self.kills}", fill="#00FF00", anchor="w", font=("Courier", 14))
        self.create_text(20, 40, text=f"HEALTH: {self.health}", fill="#00FF00", anchor="w", font=("Courier", 14))

    def game_loop(self):
        self.delete('all')
        self.move_player()
        self.raycast()
        self.draw_hud()
        self.after(50, self.game_loop)

if __name__ == "__main__":
    root = tk.Tk()
    root.attributes("-fullscreen", True)
    root.configure(bg="black")
    game = DoomClone(root)
    root.mainloop()