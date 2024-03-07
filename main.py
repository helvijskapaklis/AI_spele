# python3
import tkinter as tk
import random
class Node:
    def __init__(self, turn, num, points, div):
        self.num = num
        self.points=points
        self.turn = turn
        self.left = None
        self.right = None
        self.div = div
    
    def add_left_div2(self):
        if self.num % 2 == 0 and self.num>10 :
            temp_points=self.points.copy()
            if self.turn %2==0:
                temp_points[0]+=2
            else:
                temp_points[2]+=2
            turn = self.turn +1
            left = self.num //2
            if self.num % 5 == 0:
                temp_points[1]+=1
            self.left = Node(turn, left, temp_points, 2)

    def add_right_div3(self):
        if self.num % 3 == 0 and self.num>10 :
            temp_points=self.points.copy()
            if self.turn %2==0:
                temp_points[2]+=3
            else:
                temp_points[0]+=3
            turn = self.turn +1
            right = self.num //3
            if self.num % 5 == 0:
                temp_points[1]+=1
            self.right = Node(turn, right, temp_points, 3)
    
    def get_moves(self):
        if self.left is not None and self.right is not None:
            return [self.left , self.right]
        if self.left is not None and self.right is None:
            return [self.left]
        if self.left is None and self.right is not None:
            return [self.right]
    
    def gamestate_terminal(self):
        if self.left is None and self.right is None:
            return True
        else: return False
    

def gen_gamestates(gamestate):
    if gamestate is None:
        return
    gamestate.add_left_div2()
    gamestate.add_right_div3()
    gen_gamestates(gamestate.left)
    gen_gamestates(gamestate.right)

def can_divide_to_10_or_less(n):
    if n%3==0 and n%2==0:
        while n > 10:
            if n % 2 == 0:
                n //= 2
            elif n % 3 == 0:
                n //= 3
            else:
                return False
        return True
    return False

def gen_start(starting_num):
    while len(starting_num) < 5 :
        num = random.randint(10000,20000)
        if can_divide_to_10_or_less(num) and num not in starting_num :
            starting_num.append(num)
    return starting_num

def make_button(win, x, y, h, w, *arg1, **arg2):
    btn = tk.Button(win, *arg1, **arg2,font=("Arial",16))
    btn.place(x = x, y = y, width = w, height = h)
    return btn

def make_label(win, x, y, h, w, **arg):
    frame = tk.Frame(win, height=h, width=w)
    frame.pack_propagate(0)
    frame.place(x=x, y=y)
    label = tk.Label(frame, **arg, wraplength=w-10, font=("Arial",16))
    label.pack(fill="both", expand=1)
    return label

def create_player_labels(window):
    label_p1=make_label(window, 25, 10, 50, 175, text= "Player: 0")
    label_bank=make_label(window, 225 , 10, 50, 175, text="BANK: 0")
    label_p2=make_label(window, 425 , 10, 50, 175, text="AI: 0")
    label_turn=make_label(window,25, 85,50,125,text="")
    return label_p1, label_bank, label_p2, label_turn

def create_choices(window, starting_num):
    choice=tk.IntVar(value=10)
    player=tk.IntVar(value=10)
    ai=tk.IntVar(value=10)
    btns = []
    frame = tk.Frame(window, height = 400, width=625, bg="lightblue")
    frame.pack_propagate(0)
    frame.place(x=0,y=0)
    label = make_label(frame, 100,50,150,425, text="[" + str(starting_num[0])+"]"+" "+"[" +str(starting_num[1])+"]"+" "+"[" +str(starting_num[2])+"]"+" "+"[" +str(starting_num[3])+"]"+" "+"[" +str(starting_num[4])+"]")
    def select_choice(index):
        choice.set(index)
        for i in range(5):
            btns[i].destroy()
        label.configure(text="Choose Starting Player")
        btns.append(make_button(frame, 75, 275, 100, 200, text="You", command=lambda index=1: select_player(index)))
        btns.append(make_button(frame, 350, 275, 100, 200, text="AI", command=lambda index=2: select_player(index)))

    def select_ai(index):
        ai.set(index)
        frame.destroy()
    
    def select_player(index):
        player.set(index)
        for i in range(2):
            btns[i].destroy()
        label.configure(text="Choose AI")
        btns.append(make_button(frame, 75, 275, 100, 200, text="MINIMAX", command=lambda index=1: select_ai(index)))
        btns.append(make_button(frame, 350, 275, 100, 200, text="ALFA-BETA", command=lambda index=2: select_ai(index)))

    for i in range(5):
        btns.append(make_button(frame, 25 + i * 115, 275, 100, 100, text=str(i + 1) + ".", command=lambda index=i: select_choice(index)))

    return choice, player,ai

def hnf_value(gamestate):
    if gamestate.turn%2==0:
        return gamestate.points[2]-gamestate.points[0]
    elif gamestate.turn%2!=0:
        return gamestate.points[2]-gamestate.points[0]+gamestate.points[1]
    

def minimax(gamestate,maximizing):
    if gamestate.gamestate_terminal():
        return hnf_value(gamestate), gamestate
    
    if maximizing:
        value = float('-inf')
        possible_moves = gamestate.get_moves()
        for move in possible_moves:
            tmp,_ = minimax(move, False)
            if tmp > value:
                value = tmp
                best_move = move
    else:
        value = float('inf')
        possible_moves = gamestate.get_moves()
        for move in possible_moves:
            tmp,_ = minimax(move,True)
            if tmp < value:
                value = tmp
                best_move = move
    return value, best_move
        



def main_app(root):
    global label_p1, label_bank, label_p2, label_num, div2_btn, div3_btn, label_turn, gamestate, ai

    def call_ai():
        global ai, gamestate
        if gamestate.gamestate_terminal() == False:
            div2_btn["state"] = "disabled"
            div3_btn["state"] = "disabled"
            print("calling ai")
            if ai == 1:
                value, move = minimax(gamestate, True)
                gamestate = move
                root.after(1000,check_forwinner)
                print(value)

    def retry():
        window.destroy()
        main_app(root)
        
    def on_start():
        global gamestate,ai
        str_btn.destroy()
        choice_var, start_player_var, ai_var = create_choices(window, starting_num)
        window.wait_variable(choice_var)
        window.wait_variable(start_player_var)
        window.wait_variable(ai_var)
        choice = choice_var.get()
        start_player = start_player_var.get()
        ai = ai_var.get()  
        if (choice >=0 and choice<5) and (start_player==2 or start_player == 1) and (ai== 1 or ai ==2):
            gamestate= Node(start_player,starting_num[choice],[0,0,0],0)
            gen_gamestates(gamestate)
            on_choice()
            
    
    def on_choice():
        global label_p1, label_bank, label_p2, label_num, div2_btn, div3_btn, label_turn
        label_p1, label_bank, label_p2, label_turn=create_player_labels(window)
        label_num=make_label(window,225,85,50,175,text=gamestate.num)
        div2_btn = make_button(window,75,250,100,200,text="Divide :2", command = lambda : div2())
        div3_btn = make_button(window,350,250,100,200,text="Divide :3", command = lambda : div3())
        if gamestate.turn % 2 == 0:
            label_turn.config(text="AI's turn")
            call_ai()
        else:
            label_turn.config(text="Player's turn")
        
        

    def div2():
        global gamestate
        if gamestate.left is None:
            div2_btn["state"] = "disabled"
            return
        gamestate = gamestate.left
        check_forwinner()
        call_ai()
        
    def div3():
        global gamestate
        if gamestate.right is None:
            div3_btn["state"] = "disabled"
            return
        gamestate = gamestate.right
        check_forwinner()
        call_ai()


    def check_forwinner():
        global gamestate
        update_points()
        if gamestate.gamestate_terminal():
            if gamestate.turn%2!=0:
                gamestate.points[2]= gamestate.points[2]+gamestate.points[1]
                update_points()
            else:
                gamestate.points[0]= gamestate.points[0]+gamestate.points[1]
                update_points()
            div3_btn.destroy()
            div2_btn.destroy()
            if gamestate.points[0]==gamestate.points[2]:
                text="Its a draw !!!"
            elif gamestate.points[0]> gamestate.points[2]:
                text="Player wins !!!"
            elif gamestate.points[2]> gamestate.points[0]:
                text="AI wins !!!"
            
            print(gamestate.turn)
            label = make_label(window,225,150,50,175,text=text)
            btn = make_button(window, 250,225,50,125,text="RETRY", command= lambda: retry())
            btn2 = make_button(window, 250,300,50,125,text="EXIT", command= lambda: exit())
        else:
            if gamestate.right is not None:
                div3_btn["state"] = "normal"
            if gamestate.left is not None:
                div2_btn["state"] = "normal"



    def update_points():
        label_bank.config(text="BANK: " + str(gamestate.points[1]))
        label_num.config(text=gamestate.num)
        label_p1.config(text="Player: " + str(gamestate.points[0]))
        label_p2.config(text="AI: " + str(gamestate.points[2]))
        if not gamestate.gamestate_terminal():
            if gamestate.turn % 2 == 0:
                label_turn.config(text="AI's turn")
            else:
                label_turn.config(text="Player's turn")

    starting_num = gen_start([])
    window = tk.Frame(root, height = 400, width=625, bg="lightblue")
    window.pack_propagate(0)
    window.place(x=0,y=0)
    str_btn = make_button(window, 100, 100, 200, 425, text="START", command=lambda: on_start() )

def main():
    root = tk.Tk()
    root.title("K21 1. projekts")
    root.geometry("625x400")
    main_app(root)
    root.mainloop()
    
main()  