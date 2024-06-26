# python3
import tkinter as tk
import random
import time

class Node:
    def __init__(self, turn, num, points, div):
        # Bināra speles koka datu struktura
        
        self.num = num
        self.points=points
        self.turn = turn
        self.left = None
        self.right = None
        self.div = div
    
    def add_left_div2(self):
        # Pievieno kreiso pecteci kas ir saistits ar gajienu dalits 2
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
        # Pievieno labo pecteci kas ir saistits ar gajienu dalits 3
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
        # Atgriež pieejamos gajienus
        if self.left is not None and self.right is not None:
            return [self.left , self.right]
        if self.left is not None and self.right is None:
            return [self.left]
        if self.left is None and self.right is not None:
            return [self.right]
    
    def gamestate_terminal(self):
        # Parbauda vai speles gajiena virsotne ir galēja jeb speles beidzamais stavoklis
        if self.left is None and self.right is None:
            return True
        else: return False
    

def gen_gamestates(gamestate):
    # Izveido speles binaro koku
    if gamestate is None:
        return
    gamestate.add_left_div2()
    gamestate.add_right_div3()
    gen_gamestates(gamestate.left)
    gen_gamestates(gamestate.right)

def can_divide_to_10_or_less(n):
    # Pārbauda vai dotais skaitlis var nodalīties lidz 10 vai mazak izmantojot tikai 2 un 3
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
    # Izveido speles sākuma skaitlus
    while len(starting_num) < 5 :
        num = random.randint(10000,20000)
        if can_divide_to_10_or_less(num) and num not in starting_num :
            starting_num.append(num)
    return starting_num

def make_button(win, x, y, h, w, *arg1, **arg2):
    # Funkcija kas izveido pogas priekš grafiskās saskarsnes
    btn = tk.Button(win, *arg1, **arg2, font=("Calibri",16,"bold"))
    btn.configure(
        bg="#0D47A1",
        fg="#DCEDC8",
        border=0,
        activebackground="#1565C0",
        activeforeground="#DCEDC8", 
        highlightbackground="#1976D2",
        highlightcolor="#1976D2",
        highlightthickness=2 
    )
    btn.place(x = x, y = y, width = w, height = h)
    def on_enter(event):
        # Funkcija kas iekraso pogu kad pele ir uz tās
        btn.config(bg="#1976D2")

    def on_leave(event):
        # Funkcija kas atgriež pogu uz sākuma krasu kad pele ir noņemta no tās
        btn.config(bg="#0D47A1")

    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)
    
    return btn

def make_label(win, x, y, h, w, **arg):
    # Funkcija kas izveido grafiskas saskarsnes tekstus
    frame = tk.Frame(win, height=h, width=w)
    frame.pack_propagate(0)
    frame.place(x=x, y=y)
    label = tk.Label(frame, **arg, wraplength=w-10, font=("Calibri",16,"bold"))
    label.configure(
        bg="#0D47A1",
        fg="#DCEDC8"
    )
    label.pack(fill="both", expand=1)
    return label

def create_player_labels(window):
    # Funkcija kas izveido spele izmantotus teksta laukus
    label_p1=make_label(window, 25, 10, 50, 175, text= "Player: 0")
    label_bank=make_label(window, 225 , 10, 50, 175, text="BANK: 0")
    label_p2=make_label(window, 425 , 10, 50, 175, text="AI: 0")
    label_turn=make_label(window,25, 85,50,125,text="")
    return label_p1, label_bank, label_p2, label_turn

def create_choices(window, starting_num):
    # Funkcija kas izveido izveles laukus pirms speles sākšanas
    choice=tk.IntVar(value=10)
    player=tk.IntVar(value=10)
    ai=tk.IntVar(value=10)
    btns = []
    frame = tk.Frame(window, height = 400, width=625, bg="#04142E")
    frame.pack_propagate(0)
    frame.place(x=0,y=0)
    label = make_label(frame, 100,50,150,425, text="[" + str(starting_num[0])+"]"+" "+"[" +str(starting_num[1])+"]"+" "+"[" +str(starting_num[2])+"]"+" "+"[" +str(starting_num[3])+"]"+" "+"[" +str(starting_num[4])+"]")
    for i in range(5):
        btns.append(make_button(frame, 25 + i * 115, 275, 100, 100, text=str(i + 1) + ".", command=lambda index=i: select_choice(index)))
    
    def select_choice(index):
        # Funkcija kas uzstada izveleto sākuma ciparu un izveido speletaja gajienu secibas izveli
        choice.set(index)
        for i in range(5):
            btns[i].destroy()
        label.configure(text="Choose Starting Player")
        btns.append(make_button(frame, 75, 275, 100, 200, text="You", command=lambda index=1: select_player(index)))
        btns.append(make_button(frame, 350, 275, 100, 200, text="AI", command=lambda index=2: select_player(index)))
    
    def select_player(index):
        # Funkcija kas uzstada izveleto speletaja secibu un izveido algoritma izveli
        player.set(index)
        for i in range(2):
            btns[i].destroy()
        label.configure(text="Choose AI")
        btns.append(make_button(frame, 75, 275, 100, 200, text="MINIMAX", command=lambda index=1: select_ai(index)))
        btns.append(make_button(frame, 350, 275, 100, 200, text="ALFA-BETA", command=lambda index=2: select_ai(index)))
        
    def select_ai(index):
        # Uzstāda izvēleto algoritmu un izdzēš izvēlnes logus
        ai.set(index)
        frame.destroy()

    

    return choice, player,ai

def hnf_value(gamestate):
    # Heiristiska novertējuma funkcija
    # F = Punktu starpiba un banka +- atkarigs no pedeja gaijiena
    if gamestate.turn%2==0:
        return gamestate.points[2]-gamestate.points[0]-gamestate.points[1]
    elif gamestate.turn%2!=0:
        return gamestate.points[2]-gamestate.points[0]+gamestate.points[1]

def minimax(gamestate,maximizing):
    # minimaksa algoritma implementācija
    global node_count
    node_count+=1
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

def alfabeta(gamestate, maximizing, alpha, beta):
    # alfabeta algoritma implementācija
    global node_count
    node_count+=1
    if gamestate.gamestate_terminal():
        return hnf_value(gamestate), gamestate
    if maximizing:
        value = float('-inf')
        possible_moves = gamestate.get_moves()
        for move in possible_moves:
            tmp,_ = alfabeta(move, False, alpha, beta)
            if tmp > value:
                value = tmp
                best_move = move
            if value > alpha:
                alpha = value
            if beta <= alpha:
                break
    else:
        value = float('inf')
        possible_moves = gamestate.get_moves()
        for move in possible_moves:
            tmp,_ = alfabeta(move, True, alpha, beta)
            if tmp < value:
                value = tmp
                best_move = move
            if beta < value:
                beta = value
            if beta <= alpha:
                break
                    
    return value, best_move



def main_app(root):
    global label_p1, label_bank, label_p2, label_num, div2_btn, div3_btn, label_turn, gamestate, ai

    def call_ai():
        # Funkcija kas izsauc izvēlēto algoritmu lai tas veiktu gājienu
        global ai, gamestate, node_count
        node_count = 0 
        if gamestate.gamestate_terminal() == False:
            div2_btn["state"] = "disabled"
            div3_btn["state"] = "disabled"
            print("izsauc ai")
            if ai == 1:
                # minimax
                st = time.perf_counter()
                value, move = minimax(gamestate, True)
                et = time.perf_counter()
                elapsed_time = (et - st)*1000
                print('Gājiena izpildes laiks:', elapsed_time, 'miliseconds')
                gamestate = move
                root.after(1000,check_forwinner)
                print("Virsotnes apmeklētas: ", node_count)
                print("heiristiskais novērtējums: ", value)
            if ai == 2:
                # alfa beta
                st = time.perf_counter()
                value, move = alfabeta(gamestate, True, float('-inf'), float('inf'))
                et = time.perf_counter()
                elapsed_time = (et - st)*1000
                print('Gājiena izpildes laiks:', elapsed_time, 'miliseconds')
                gamestate = move
                root.after(1000,check_forwinner)
                print("Virsotnes apmeklētas: ", node_count)
                print("heiristiskais novērtējums: ", value)

    def retry():
        # pogas retry funkcija kas izveido jaunu speli
        window.destroy()
        main_app(root)
        
    def on_start():
        # uz start pogas nospiešanas izsauc izveles funkcijas un izveido speles koku
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
        # Funkcija kas izveido galveno speles ekranu un ja ai ir jāsāk pirmajam tad izsauc to
        global label_p1, label_bank, label_p2, label_num, div2_btn, div3_btn, label_turn
        label_p1, label_bank, label_p2, label_turn=create_player_labels(window)
        label_num=make_label(window,225,85,50,175,text=gamestate.num)
        div2_btn = make_button(window,75,250,100,200,text="Divide by 2", command = lambda : div2())
        div3_btn = make_button(window,350,250,100,200,text="Divide by 3", command = lambda : div3())
        if gamestate.turn % 2 == 0:
            label_turn.config(text="AI's turn")
            call_ai()
        else:
            label_turn.config(text="Player's turn")
        
        

    def div2():
        # Funkcija kas nobīda spēles stavokli uz koka kreiso pēcteci un pārbauda vai spēle nav beigusies un izsauc ai
        global gamestate
        if gamestate.left is None:
            div2_btn["state"] = "disabled"
            return
        gamestate = gamestate.left
        check_forwinner()
        call_ai()
        
    def div3():
        # Funkcija kas nobīda spēles stavokli uz koka labo pēcteci un pārbauda vai spēle nav beigusies un izsauc ai
        global gamestate
        if gamestate.right is None:
            div3_btn["state"] = "disabled"
            return
        gamestate = gamestate.right
        check_forwinner()
        call_ai()


    def check_forwinner():
        # Logika kas pārbauda vai spele nav beigusies un ja ir tad
        # tad izveido spels beigu ekranu un pieskaita bankas punktus tam kas ir pedējais gajiens
        # un izvada uzvarētaju
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
            
            
            label = make_label(window,225,150,50,175,text=text)
            btn = make_button(window, 250,225,50,125,text="RETRY", command= lambda: retry())
            btn2 = make_button(window, 250,300,50,125,text="EXIT", command= lambda: exit())
        else:
            if gamestate.right is not None:
                div3_btn["state"] = "normal"
            if gamestate.left is not None:
                div2_btn["state"] = "normal"



    def update_points():
        # Funkcija kas atjauno grafiskas saskarsnes ekranu ar patreizējo spēles stavokli
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
    window = tk.Frame(root, height = 400, width=625, bg="#04142E")
    window.pack_propagate(0)
    window.place(x=0,y=0)
    str_btn = make_button(window, 100, 100, 200, 425, text="START", command=lambda: on_start() )

def main():
    # Funkcija kas inicializē speli un tās logu
    root = tk.Tk()
    root.title("K21 1. projekts")
    root.geometry("625x400")
    main_app(root)
    root.mainloop()
    
if __name__ == "__main__":
    # Funkcija kas iniciālize kodu
    main()  