# python3
import tkinter as tk
import random
class Node:
    def __init__(self, turn, num, points):
        self.num = num
        self.points=points
        self.turn = turn
        self.left = None
        self.right = None
    
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
            self.left = Node(turn, left, temp_points)

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
            self.right = Node(turn, right, temp_points)
    

def gen_gamestates(gamestate):
    if gamestate is None:
        return
    gamestate.add_left_div2()
    gamestate.add_right_div3()
    gen_gamestates(gamestate.left)  
    gen_gamestates(gamestate.right)


def gen_start(starting_num):
    while len(starting_num) < 5 :
        temp = random.randint(1,10)
        while(1):
            rand = random.choice([True, False])
            if rand == True:
                temp=temp*2
            else:
                temp=temp*3
            if temp > 10000 and temp<20000:
                starting_num.append(temp)
            if temp>20000:
                break
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
    label_p1=make_label(window, 25, 10, 50, 175, text= "Player 1: 0")
    label_bank=make_label(window, 225 , 10, 50, 175, text="BANK: 0")
    label_p2=make_label(window, 425 , 10, 50, 175, text="Player 2: 0")
    label_turn=make_label(window,25, 85,50,125,text="")
    return label_p1, label_bank, label_p2, label_turn

def create_choices(window, starting_num):
    choice=tk.IntVar(value=10)
    player=tk.IntVar(value=10)
    btns = []
    frame = tk.Frame(window, height = 400, width=625, bg="lightblue")
    frame.pack_propagate(0)
    frame.place(x=0,y=0)
    label = make_label(frame, 100,50,150,425, text=starting_num)
    def select_choice(index):
        choice.set(index)
        for i in range(5):
            btns[i].destroy()
        label.configure(text="Choose Player")
        btns.append(make_button(frame, 75, 275, 100, 200, text="1" + ".", command=lambda index=1: select_player(index)))
        btns.append(make_button(frame, 350, 275, 100, 200, text="2" + ".", command=lambda index=2: select_player(index)))

    
    def select_player(index):
        player.set(index)
        frame.destroy()

    for i in range(5):
        btns.append(make_button(frame, 25 + i * 115, 275, 100, 100, text=str(i + 1) + ".", command=lambda index=i: select_choice(index)))

    return choice, player



def main_app(root):
    global label_p1, label_bank, label_p2, label_num, div2_btn, div3_btn, label_turn, gamestate, ai_turn
    def retry():
        window.destroy()
        main_app(root)
        
    def on_start():
        global gamestate, ai_turn
        str_btn.destroy()
        choice_var, counter_var = create_choices(window, starting_num)
        window.wait_variable(choice_var)
        window.wait_variable(counter_var)
        choice = choice_var.get()
        counter = counter_var.get()
        if choice >=0 and choice<5 and counter==2 or counter == 1:
            gamestate= Node(counter,starting_num[choice],[0,0,0])
            ai_turn = counter
            gen_gamestates(gamestate)
            on_choice()
            
    
    def on_choice():
        global label_p1, label_bank, label_p2, label_num, div2_btn, div3_btn, label_turn
        label_p1, label_bank, label_p2, label_turn=create_player_labels(window)
        label_num=make_label(window,225,85,50,175,text=gamestate.num)
        if gamestate.turn % 2 == 0:
            label_turn.config(text="Player 2 turn")
        else:
            label_turn.config(text="Player 1 turn")
        
        div2_btn = make_button(window,75,250,100,200,text="Divide :2", command = lambda : div2())
        div3_btn = make_button(window,350,250,100,200,text="Divide :3", command = lambda : div3())

    def div2():
        global gamestate
        if gamestate.left is None:
            return
        gamestate = gamestate.left
        check_forwinner()
        update_points()
        
    def div3():
        global gamestate
        if gamestate.right is None:
            return
        gamestate = gamestate.right
        check_forwinner()
        update_points()

    def check_forwinner():
        global gamestate
        if gamestate.num %3 !=0 and gamestate.num%2 !=0 or gamestate.num <=10:
            if gamestate.turn%2==0:
                gamestate.points[2]= gamestate.points[2]+gamestate.points[1]
            else:
                gamestate.points[0]= gamestate.points[0]+gamestate.points[1]
            update_points()
            text="Its a draw !!!"
            div3_btn.destroy()
            div2_btn.destroy()

            if gamestate.points[0]> gamestate.points[2]:
                text="Player 1 wins !!!"

            if gamestate.points[2]> gamestate.points[0]:
                text="Player 2 wins !!!"

            label = make_label(window,225,150,50,175,text=text)
            btn = make_button(window, 250,225,50,125,text="RETRY", command= lambda: retry())
            btn2 = make_button(window, 250,300,50,125,text="EXIT", command= lambda: exit())



    def update_points():
        label_bank.config(text="BANK: " + str(gamestate.points[1]))
        label_num.config(text=gamestate.num)
        label_p1.config(text="Player 1: " + str(gamestate.points[0]))
        label_p2.config(text="Player 2: " + str(gamestate.points[2]))
        if gamestate.turn % 2 == 0:
            label_turn.config(text="Player 2 turn")
        else:
            label_turn.config(text="Player 1 turn")

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