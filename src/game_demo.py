import pygame
import sys
import os
import re
from pygame.locals import *
from openai import OpenAI

# OpenAI配置
# 在运行前设置环境变量：
# export OPENAI_API_KEY="your-api-key"
# export OPENAI_ORGANIZATION="your-org-id"  

# 初始化pygame
pygame.init()

# OpenAI配置
client = OpenAI()

# 常量定义
GAME_WIDTH = 800
GAME_HEIGHT = 400  # 游戏区域高度
CHAT_HEIGHT = 300  # 聊天区域高度
WINDOW_WIDTH = GAME_WIDTH
WINDOW_HEIGHT = GAME_HEIGHT + CHAT_HEIGHT
TILE_SIZE = 40

# 颜色定义
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BROWN = (139, 69, 19)
GREEN = (34, 139, 34)
LIGHT_GRAY = (240, 240, 240)

# 设置窗口
DISPLAYSURF = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Work With Farmer Louise')

class Farmer:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = TILE_SIZE
        self.height = TILE_SIZE * 2
        self.body_color = BROWN
        self.skin_color = (255, 218, 185)
        self.hat_color = (139, 69, 19)
        self.understands_movement = False
        self.understands_directions = False
        self.understands_distance = False
        self.speed = 2
        self.step_size = TILE_SIZE  # 一步的大小
        self.current_movement = None
        self.movement_queue = []  # 存储多个移动指令
        
    def queue_movement(self, direction, distance=None):
        """添加移动指令到队列"""
        if not self.understands_movement:
            return
            
        target_x = self.x
        target_y = self.y
        
        # 如果队列中有移动指令，从最后一个指令的目标位置开始计算
        if self.movement_queue:
            last_movement = self.movement_queue[-1]
            target_x = last_movement['target_x']
            target_y = last_movement['target_y']
        
        # 如果理解距离，使用指定的步数，否则默认移动一步
        steps = distance if self.understands_distance else 1
        move_distance = steps * self.step_size
        
        new_target_x = target_x
        new_target_y = target_y
        
        if direction == 'left':
            new_target_x = max(0, target_x - move_distance)
        elif direction == 'right':
            new_target_x = min(GAME_WIDTH - self.width, target_x + move_distance)
        elif direction == 'up':
            new_target_y = max(0, target_y - move_distance)
        elif direction == 'down':
            new_target_y = min(GAME_HEIGHT - self.height, target_y + move_distance)
            
        self.movement_queue.append({
            'target_x': new_target_x,
            'target_y': new_target_y
        })
    






    def start_movement(self, direction, distance=None):
        if not self.understands_movement:
            return
            
        target_x = self.x
        target_y = self.y
        
        # 如果理解距离，使用指定的步数，否则默认移动一步
        steps = distance if self.understands_distance else 1
        move_distance = steps * self.step_size
        
        if direction == 'left':
            target_x = max(0, self.x - move_distance)
        elif direction == 'right':
            target_x = min(GAME_WIDTH - self.width, self.x + move_distance)
        elif direction == 'up':
            target_y = max(0, self.y - move_distance)
        elif direction == 'down':
            target_y = min(GAME_HEIGHT - self.height, self.y + move_distance)
            
        self.current_movement = {
            'target_x': target_x,
            'target_y': target_y
        }

    def update(self):
        # 如果当前没有移动指令但队列中有指令，取出下一个指令
        if not self.current_movement and self.movement_queue:
            self.current_movement = self.movement_queue.pop(0)
            
        if not self.current_movement:
            return
            
        target_x = self.current_movement['target_x']
        target_y = self.current_movement['target_y']
        
        # 计算移动方向
        dx = target_x - self.x
        dy = target_y - self.y
        
        # 如果距离很小，就认为已到达
        if abs(dx) < self.speed and abs(dy) < self.speed:
            self.x = target_x
            self.y = target_y
            self.current_movement = None
            return
            
        # 计算移动方向并应用速度
        distance = (dx * dx + dy * dy) ** 0.5
        if distance > 0:
            self.x += (dx / distance) * self.speed
            self.y += (dy / distance) * self.speed

            
    def draw(self):
        # 画帽子（梯形）
        hat_points = [
            (self.x - 5, self.y),
            (self.x + self.width + 5, self.y),
            (self.x + self.width - 5, self.y - 10),
            (self.x + 5, self.y - 10)
        ]
        pygame.draw.polygon(DISPLAYSURF, self.hat_color, hat_points)
        
        # 画头（圆形）
        head_radius = self.width // 2
        head_center = (self.x + self.width // 2, self.y + head_radius)
        pygame.draw.circle(DISPLAYSURF, self.skin_color, head_center, head_radius)
        
        # 画身体（梯形，像连衣裙）
        body_points = [
            (self.x, self.y + self.width),
            (self.x + self.width, self.y + self.width),
            (self.x + self.width + 10, self.y + self.height),
            (self.x - 10, self.y + self.height)
        ]
        pygame.draw.polygon(DISPLAYSURF, self.body_color, body_points)

        # 画眼睛
        eye_color = BLACK
        left_eye = (self.x + self.width // 3, self.y + head_radius)
        right_eye = (self.x + (self.width * 2 // 3), self.y + head_radius)
        pygame.draw.circle(DISPLAYSURF, eye_color, left_eye, 2)
        pygame.draw.circle(DISPLAYSURF, eye_color, right_eye, 2)
        
        # 画笑容
        smile_rect = pygame.Rect(
            self.x + self.width//3, 
            self.y + head_radius, 
            self.width//3, 
            self.width//4
        )
        pygame.draw.arc(DISPLAYSURF, eye_color, smile_rect, 0, 3.14, 2)

class Box:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = TILE_SIZE
        self.height = TILE_SIZE
        self.color = BROWN
        self.movable = False
        
    def draw(self):
        pygame.draw.rect(DISPLAYSURF, self.color,
                        (self.x, self.y, self.width, self.height))
        
    def move(self, dx, dy):
        if self.movable:
            self.x += dx
            self.y += dy

class ChatBox:
    def __init__(self):
        self.rect = pygame.Rect(10, GAME_HEIGHT + 10, WINDOW_WIDTH - 20, 40)
        self.color = WHITE
        self.text = ""
        self.font = pygame.font.Font(None, 32)
        self.active = False
        
    def handle_event(self, event):
        if event.type == MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = True
            else:
                self.active = False
        elif event.type == KEYDOWN and self.active:
            if event.key == K_RETURN and self.text.strip():  # 只在有文本时才发送
                message = self.text
                self.text = ""
                return message
            elif event.key == K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode
        return None
    
    def draw(self):
        pygame.draw.rect(DISPLAYSURF, self.color, self.rect)
        if self.active:
            color = GREEN
        else:
            color = BLACK
        pygame.draw.rect(DISPLAYSURF, color, self.rect, 2)
        
        text_surface = self.font.render(self.text, True, BLACK)
        DISPLAYSURF.blit(text_surface, (self.rect.x + 5, self.rect.y + 5))

class Game:
    def __init__(self):
        self.farmer = Farmer(GAME_WIDTH//4, GAME_HEIGHT//2)
        self.box = Box(GAME_WIDTH//2, GAME_HEIGHT//2)
        self.chat_box = ChatBox()
        self.messages = []


        self.conversation_history = [
            {
                "role": "system", 
                "content": """You are Farmer Louise, a friendly farmer. 
                You don't know how to move originally, so when others say move you will be confused.
                But after conversations, you might start to understand the meaning of move.
                Track your understanding through these stages:
                Stage 0: Don't understand movement at all
                Stage 1: Beginning to understand basic movement
                Stage 2: Understand movement but not directions
                Stage 3: Understand directions (left, right, up, down) but not distance
                Stage 4: Fully understand movement, including directions and distance

                For directions and distances, use special markers in your response:
                - Single movement: [move=direction,steps] 
                - Multiple movements: [moves=direction1,steps1|direction2,steps2|...]

                Example responses:
                "Walk? I'm not sure what you mean... [stage=0]"
                "Oh, I can move my legs to walk! [stage=1]"
                "I can walk, but where should I go? [stage=2]"
                "Oh, you want me to go right! [stage=3][move=right,1]"
                "I'll walk 5 steps to the right! [stage=4][move=right,5]"
                "I'll go down 2 steps and then right 5 steps! [stage=4][moves=down,2|right,5]"

                Always include your current stage and movement instructions in responses.
                When understanding multiple movements, use the [moves=...] format.
                Respond naturally to user instructions while maintaining character."""
            }
        ]

    def draw_chat_area(self):
        # 绘制聊天区域背景
        chat_area = pygame.Rect(0, GAME_HEIGHT, WINDOW_WIDTH, CHAT_HEIGHT)
        pygame.draw.rect(DISPLAYSURF, LIGHT_GRAY, chat_area)
        pygame.draw.line(DISPLAYSURF, BLACK, (0, GAME_HEIGHT), (WINDOW_WIDTH, GAME_HEIGHT))
        
        # 绘制消息历史
        font = pygame.font.Font(None, 24)
        y = self.chat_box.rect.bottom + 20  # 从输入框下方开始显示消息
        
        # 只显示最近3条消息
        display_messages = self.messages[-3:]
        
        for msg, resp in display_messages:
            msg_surface = font.render(f"You: {msg}", True, BLACK)
            resp_surface = font.render(f"Louise: {resp}", True, BROWN)
            
            DISPLAYSURF.blit(msg_surface, (20, y))
            DISPLAYSURF.blit(resp_surface, (20, y + 25))
            y += 70

    def draw_game_area(self):
        # 绘制游戏区域（纯白背景）
        game_area = pygame.Rect(0, 0, GAME_WIDTH, GAME_HEIGHT)
        pygame.draw.rect(DISPLAYSURF, WHITE, game_area)
        
        # 绘制游戏元素
        self.farmer.draw()
        self.box.draw()






    def process_message(self, message):
        try:
            self.conversation_history.append({"role": "user", "content": message})
            
            completion = client.chat.completions.create(
                model="gpt-4-turbo",
                messages=self.conversation_history,
                temperature=0.7,
                max_tokens=60
            )
            
            full_response = completion.choices[0].message.content
            
            # 解析理解阶段
            stage_match = re.search(r'\[stage=(\d)\]', full_response)
            
            # 解析多个移动指令
            moves_match = re.search(r'\[moves=(.*?)\]', full_response)
            # 解析单个移动指令
            move_match = re.search(r'\[move=(\w+),(\d+)\]', full_response)
            
            # 清理回复中的所有标记
            response = re.sub(r'\[.*?\]', '', full_response).strip()
            
            if stage_match:
                understanding_stage = int(stage_match.group(1))
                
                # 更新理解状态
                if understanding_stage >= 2:
                    self.farmer.understands_movement = True
                if understanding_stage >= 3:
                    self.farmer.understands_directions = True
                if understanding_stage >= 4:
                    self.farmer.understands_distance = True
                    
                # 处理多个移动指令
                if self.farmer.understands_directions and moves_match:
                    move_commands = moves_match.group(1).split('|')
                    for cmd in move_commands:
                        direction, steps = cmd.split(',')
                        self.farmer.queue_movement(direction.strip(), int(steps))
                # 处理单个移动指令
                elif self.farmer.understands_directions and move_match:
                    direction = move_match.group(1)
                    steps = int(move_match.group(2))
                    self.farmer.queue_movement(direction, steps)
            
            self.conversation_history.append({"role": "assistant", "content": full_response})
            return response
            
        except Exception as e:
            print(f"API Error: {str(e)}")
            import traceback
            print(traceback.format_exc())
            return "Sorry, I encountered an error. Please try again."


    def update_game(self):
        self.farmer.update()
    
    def run(self):
        clock = pygame.time.Clock()
        
        while True:
            DISPLAYSURF.fill(WHITE)
            clock.tick(60)
            
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                    
                message = self.chat_box.handle_event(event)
                if message:
                    response = self.process_message(message)
                    self.messages.append((message, response))
            
            # 更新游戏状态
            self.update_game()
            
            # 分别绘制游戏区域和聊天区域
            self.draw_game_area()
            self.draw_chat_area()
            self.chat_box.draw()
            
            pygame.display.update()

if __name__ == '__main__':
    game = Game()
    game.run()