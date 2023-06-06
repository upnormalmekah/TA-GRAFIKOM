from ursina import * #import semua yang ada di lib ursina 
from random import randint #import randint dari lib random

def input(key): #membuat fungsi gerak
    global peluru, run #memanggil variabel global

    if run:
        if key=="up arrow" or key=="up arrow hold":
            pesawat.y+=.25 #buat fungsi gerakan pesawat 0.25 keatas 
        if key=="down arrow" or key=="down arrow hold":
            pesawat.y-=.25 #buat fungsi gerakan pesawat 0.25 kebawah
        if key=="space": #buat fungsi tembakan
            Audio("assets/kyah.mp3")
            peluru=Peluru()
            pelurus.append(peluru)

def update(): #fungsi perubahan#fungsi perubahan dan logika permainan
    global pelurus, text, score, run #memanggil variabel global

    if run:
        for peluru in pelurus: #buat peluru jadi banyak mengguanakan looping
            peluru.x+=time.dt*peluru.speed #buat gerakan peluru dengan mengalikan waktu dan kecepatan

            hit_info=peluru.intersects()#buat mendeteksi tabrakan pada objek peluru
            if hit_info.hit: #kondisi jika objek peluru bertabrakan
                peluru.z=1 #ngubah sumbu z pada objek peluru menjadi 1
                if hit_info.entity in musuhs: #kondisi jika objek peluru menabrak objek musuh
                    score+=1 #menambahkan jumlah sebesar 1 pada score
                    text.y=1 #ngubah sumbu y pada text menjadi 1
                    text=Text(text=f"Score: {score}", 
                          position=(-.65, .4), 
                          origin=(0,0), 
                          scale=2,
                          color=color.yellow, background=True) #menampilkan text score

                    CreateBubbles(hit_info.entity.x, hit_info.entity.y) #membuat fungsi untuk menampilkan gelembung
                    hit_info.entity.x=randint(8,14) #menambahkan random integer pada sumbu x dari 8 - 14
                    hit_info.entity.y=randint(-36,36)*.14 #menambahkan random integer pada sumbu y dari (-36) - 36 dikali 0.14
    
        for musuh in musuhs: #looping untuk mengedit setiap musuh pada setiap array musuh
            musuh.x-=time.dt*musuh.speed #buat gerakan musuh dengan mengalikan waktu dan kecepatan
            if musuh.x<-randint(8,14): #kondisi ketika sumbu x objek musuh merupakan angka random dari 8 - 14
                musuh.x=randint(8,14) #menambahkan random integer pada sumbu x musuh dari 8 - 14
                musuh.y=randint(-36,36)*.14 #menambahkan random integer pada sumbu y musuh dari (-36) - 36 dikali 0.14
                musuh.speed=randint(1,3) #menambahkan random integer pada kecepatan musuh dari 1-3

    hit_info=pesawat.intersects()#buat mendeteksi tabrakan pada objek peluru
    if hit_info.hit: #kondisi jika pesawat bertabrakan
        run=False #jika kondisi terpenuhi maka program akan close
        Entity(model="quad", 
               scale=(20,10), 
               texture="assets/background.png",
               z=.1)
        Text(text="Pesawatmu Nabrak! Reload Gamenya!",
             origin=(0,0),
             scale=2,
             color=color.yellow,
             background=True) #membuat text seperti game over

class Bubbles(Entity): #membuat class untuk gelembung
    def __init__(self,x,y): #menginisialisasi (menetapkan nilai awal) objek yang dibuat dari sebuah kelas
        super().__init__() #untuk memanggil metode dari kelas induk dan melakukan inisialisasi awal untuk objek turunan.
        self.model="circle" #menentukan model atau bentuk visual dari sebuah entitas menjadi bulat.
        self.scale=.5 #mengubah scale objek menjadi 0.5
        self.x=x #memasukan nilai parameter x ke sumbu x pada objek 
        self.y=y #memasukan nilai parameter y ke sumbu y pada objek 

    def update(self): #fungsi perubahan pada objek gelembung
        self.x+=random.randint(-2, 2)/100 #menambahkan random integer pada sumbu x dari (-2) - 2 dibagi 100
        self.y+=random.randint(0, 2)/50 #menambahkan random integer pada sumbu y dari 0 - 2 dibagi 50
        self.scale-=.008 #mengubah scale objek menjadi 0.008
        if self.scale <= .005: #jika scale objek lebih kecil dari 0.005
            destroy(self) #hancurkan objek

class Musuh(Entity): #membuat class untuk Musuh
    def __init__(self, x, y, speed): #menginisialisasi (menetapkan nilai awal) objek yang dibuat dari sebuah kelas
        super().__init__() #untuk memanggil metode dari kelas induk dan melakukan inisialisasi awal untuk objek turunan.
        self.model="quad" #menentukan model atau bentuk visual dari sebuah entitas menjadi persegi.
        self.scale=(1, 1) #mengubah scale objek pada sumbu x dan y
        self.x=x #memasukan nilai parameter x ke sumbu x pada objek 
        self.y=y #memasukan nilai parameter y ke sumbu y pada objek 
        self.speed=speed #memasukan nilai parameter speed ke speed dalam objek
        self.texture="assets/Logo_PDI.png" #memasukan texture dari objek musuh berupa gambar banteng
        self.collider="box" #membuat kolisi area yang bisa bertabrakan dengan objek lain

class Peluru(Entity): #membuat class untuk Peluru
    def __init__(self):#menginisialisasi (menetapkan nilai awal) objek yang dibuat dari sebuah kelas
        super().__init__() #untuk memanggil metode dari kelas induk dan melakukan inisialisasi awal untuk objek turunan.
        self.model="quad" #menentukan model atau bentuk visual dari sebuah entitas menjadi persegi.
        self.texture="assets/peluru.png" #memasukan texture dari objek musuh berupa gambar banteng
        self.scale=.8  #mengubah scale objek menjadi 0.8
        self.x=pesawat.x+1.4 #memasukan nilai sumbu x pesawat ditambah 1.4 ke sumbu x pada objek 
        self.y=pesawat.y-.18 #memasukan nilai sumbu y pesawat ditambah 0.18 ke sumbu x pada objek 
        self.speed=3 #memasukan nilai speed sebesar 3
        self.collider="box" #membuat kolisi area yang bisa bertabrakan dengan objek lain

def CreateBubbles(x, y): #fungsi membuat gelembung
    num=10
    e=[None]*num
    for i in range(num):
        e[i]=Bubbles(x,y)

app = Ursina() #fungsi utama ursina
bg = Entity(
    model="quad",
    scale=(20,10),
    texture = "assets/background.png",
    z=.1
    ) #membuat background

pesawat=Animation(
    "assets/pesawat", 
    collider="box", 
    scale=(2,1),
    x=-3,
    y=1
    ) #membuat pesawat

num=8
musuhs=[None]*num #array musuh
pelurus=[] #array peluru
score=0
run=True

text = Text(text=f"Score: {score}", position=(-.65, .4), origin=(0,0), scale=2, color=color.yellow, background=True) # membuat text score

for i in range(num): #membuat musuh menjadi banyak menggunakan looping
    x=randint(8, 14)
    y=randint(-36, 36)*.1
    speed=randint(1,3)
    musuhs[i]=Musuh(x,y,speed) #memanggil class musuh

app.run() #menjalankan fungsi utama ursina