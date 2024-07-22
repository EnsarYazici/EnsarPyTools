import flet as ft
from time import sleep
import json
# from flet import Page, Text

def main(page:ft.Page):

    def expandTabContainer(e):
        if e.control.selected_index == 0:
            cont_Input.height = 225
        else:
            cont_Input.height = 350
        page.update()

    # Öğeleri options.json dosyasından okuma
    def load_items():
        with open("options.json", "r") as file:
            data = json.load(file)
            items = data.get("items", [])
            for item_text in items:
                item = ft.Row(
                    controls=[
                        ft.IconButton(icon=ft.icons.DELETE, on_click=lambda e, t=item_text: remove_item(t),icon_color="#d4d4da"),
                        ft.Text(item_text,color="#d4d4da")
                    ],
                    key=item_text
                )
                lv.controls.append(item)

    # Öğeyi options.json dosyasından silme
    def remove_item(item_key):
        # ListView'den öğeyi kaldır
        lv.controls = [item for item in lv.controls if item.key != item_key]
        
        # options.json dosyasından öğeyi kaldır
        with open("options.json", "r") as file:
            data = json.load(file)
        data["items"] = [item for item in data["items"] if item != item_key]
        with open("options.json", "w") as file:
            json.dump(data, file, indent=4)
        page.update()
    
    page.title = "Basic elevated buttonsssss"
    page.icon = "./images/SbmBot.ico"
    page.bgcolor = ft.colors.AMBER_100
    page.padding = 0


    s = ft.TextField("otuzbirci",icon=ft.icons.PASSWORD,password=True,can_reveal_password=True,hint_text="E-Devlet Şifresi",label="E-Devlet Şifresi",color=ft.colors.BLUE_800,label_style=ft.TextStyle(color=ft.colors.WHITE70),hint_style=ft.TextStyle(color=ft.colors.BLUE_800),border_color=ft.colors.BLUE_800,expand=1,expand_loose=1)
    tc = ft.TextField("24992234274",icon=ft.icons.PERSON,hint_text="TC Kimlik Numarası",label="TC Kimlik Numarası",color=ft.colors.BLUE_800,label_style=ft.TextStyle(color=ft.colors.WHITE70),hint_style=ft.TextStyle(color=ft.colors.BLUE_800),border_color=ft.colors.BLUE_800,expand=1,expand_loose=1)
    p = ft.TextField("otuzbirci",icon=ft.icons.PASSWORD,password=True,can_reveal_password=True,hint_text="E-İmza PIN Kodu",label="E-İmza PIN Kodu",color=ft.colors.BLUE_800,label_style=ft.TextStyle(color=ft.colors.WHITE70),hint_style=ft.TextStyle(color=ft.colors.BLUE_800),border_color=ft.colors.BLUE_800,expand=1,expand_loose=1)
    em = ft.TextField("ensar.yazici",icon=ft.icons.ASSIGNMENT_IND,hint_text="Kullanıcı Adı",label="Kullanıcı Adı",color=ft.colors.BLUE_800,label_style=ft.TextStyle(color=ft.colors.WHITE70),hint_style=ft.TextStyle(color=ft.colors.BLUE_800),border_color=ft.colors.BLUE_800,expand=1,expand_loose=1)
    
    lv_EMP = ft.ListView(expand=1, spacing=10, padding=20)
    lv_EMP.controls.append(em)
    lv_EMP.controls.append(p)
    lv_EMP.controls.append(tc)
    lv_EMP.controls.append(s)
    lv_TCS = ft.ListView(expand=1, spacing=10, padding=20)
    lv_TCS.controls.append(tc)
    lv_TCS.controls.append(s)

    tabs_Input = ft.Tabs(
        selected_index=0,
        tabs=[
            ft.Tab(
                text="E-Devlet",
                content=lv_TCS,
            ),
            ft.Tab(
                text="E-İmza",
                content=lv_EMP
            )
        ],
        expand=1,
        tab_alignment=ft.TabAlignment.CENTER,
        on_change=expandTabContainer,
        overlay_color=ft.colors.BLUE_800,
        label_color=ft.colors.BLUE_800,
        divider_color=ft.colors.BLUE_800,
        indicator_color=ft.colors.BLUE_800,
        unselected_label_color="#d4d4da",
        expand_loose=1
    )

    
    cont_Input = ft.Container(
                    # tb = ft.TextField(label="Textbox with 'change' event:",on_change=textbox_changed),
                    content=tabs_Input,
                    margin=10,
                    padding=10,
                    alignment=ft.alignment.top_center,
                    bgcolor=ft.colors.with_opacity(0.5,ft.colors.BLACK),
                    border_radius=10,
                    expand=1,
                    expand_loose=1
                    
                )
    
    lv = ft.ListView(expand=1, spacing=10, padding=20)

    # Tamamlanmamislari yukle
    load_items()


    # ListView'i bir Container içine alma

    tabs_Tamamlanmamis = ft.Tabs(
        selected_index=0,
        tabs=[
            ft.Tab(
                text="Tamamlanmamış",
                content=lv,
            )
        ],
        expand=1,
        tab_alignment=ft.TabAlignment.CENTER,
        overlay_color=ft.colors.BLUE_800,
        label_color="#d4d4da",
        divider_color=ft.colors.BLUE_800,
        indicator_color=ft.colors.BLUE_800,
        unselected_label_color="#d4d4da",
        expand_loose=1

    )
    cont_Tamamlanmamis = ft.Container(
                   
                    content=tabs_Tamamlanmamis,
                    margin=10,
                    padding=10,
                    alignment=ft.alignment.bottom_center,
                    bgcolor=ft.colors.with_opacity(0.5,ft.colors.BLACK),
                    border_radius=10,
                    expand=1,
                    expand_loose=1
                )

    rootcol1 = ft.Column(spacing=0, controls=[cont_Input,cont_Tamamlanmamis],alignment=ft.MainAxisAlignment.CENTER,horizontal_alignment=ft.CrossAxisAlignment.CENTER,expand=1,expand_loose=1)
    
    logger = ft.TextField("asdasdasd",multiline=True,border_color=ft.colors.BLUE_800,text_style=ft.TextStyle(size=10),read_only=True)
    cont_Logger = ft.Container(
                
                content=logger,
                margin=10,
                padding=1.5,
                alignment=ft.alignment.top_center,
                bgcolor=ft.colors.with_opacity(0.5,ft.colors.BLACK),
                border_radius=10,
                expand=1,
                expand_loose=1
                
            )
    

    b = ft.IconButton(
        icon=ft.icons.PLAY_CIRCLE_OUTLINED, data=0,expand=1,expand_loose=1,icon_size=100,icon_color="#d4d4da"
    )

    x = ft.IconButton(
        icon=ft.icons.STOP_CIRCLE_OUTLINED, data=0,expand=1,expand_loose=1,icon_size=100,icon_color=ft.colors.BLUE_800
    )

    df = ft.TextField("asdasdasd/asd/asd",border_color=ft.colors.BLUE_800,read_only=True,expand=1,expand_loose=1)
    dfb = ft.IconButton(
        icon=ft.icons.DRIVE_FOLDER_UPLOAD_SHARP, data=0,expand=0.5,expand_loose=1,icon_size=60,icon_color="#d4d4da"
    )

    u = ft.TextField("",hint_text="GG.AA.YYY, SS:DD",label="Başlangıç",color=ft.colors.BLUE_800,label_style=ft.TextStyle(color=ft.colors.WHITE70),hint_style=ft.TextStyle(color=ft.colors.BLUE_800,size=10),border_color=ft.colors.BLUE_800,expand=1,expand_loose=1)
    d = ft.TextField("",icon=ft.icons.DOUBLE_ARROW_OUTLINED,hint_text="GG.AA.YYY, SS:DD",label="Bitiş",color=ft.colors.BLUE_800,label_style=ft.TextStyle(color=ft.colors.WHITE70),hint_style=ft.TextStyle(color=ft.colors.BLUE_800,size=10),border_color=ft.colors.BLUE_800,expand=1,expand_loose=1)
    
    row_dfb =  ft.Row(spacing=10, controls=[dfb,df],alignment=ft.MainAxisAlignment.CENTER,vertical_alignment=ft.CrossAxisAlignment.CENTER,expand=1,expand_loose=1)
    
    row_ud =  ft.Row(spacing=10, controls=[u,d],alignment=ft.MainAxisAlignment.CENTER,vertical_alignment=ft.CrossAxisAlignment.CENTER,expand=1,expand_loose=1)
    
    row_S =  ft.Row(spacing=10, controls=[b,x],alignment=ft.MainAxisAlignment.CENTER,vertical_alignment=ft.CrossAxisAlignment.CENTER,expand=1,expand_loose=1)
    col_SD = ft.Column(spacing=0, controls=[row_S,row_dfb,row_ud],alignment=ft.MainAxisAlignment.CENTER,horizontal_alignment=ft.CrossAxisAlignment.CENTER,expand=1,expand_loose=1)
    cont_Play = ft.Container(

                content=col_SD,
                margin=10,
                padding=10,
                alignment=ft.alignment.top_center,
                bgcolor=ft.colors.with_opacity(0.5,ft.colors.BLACK),
                border_radius=10,
                expand=1,
                expand_loose=1
                
            )
    

    f = ft.Text("Filing Bird", size=25)
    v = ft.Text("PTT v1.6.0", size=15)

    col_IMGP = ft.Column(spacing=10, controls=[cont_Play,f,v],alignment=ft.MainAxisAlignment.CENTER,horizontal_alignment=ft.CrossAxisAlignment.CENTER,expand=1,expand_loose=1)


    rootRow= ft.Row(spacing=0, controls=[rootcol1,cont_Logger,col_IMGP],vertical_alignment=ft.CrossAxisAlignment.STRETCH,expand=1,expand_loose=1)




    # Gradient arka plan için bir Container oluştur
    gradient_container = ft.Container(
        content=ft.Column(
            controls=[
                rootRow
            ],
        ),
        gradient=ft.LinearGradient(
            begin=ft.alignment.bottom_right,
            end=ft.alignment.top_left,
            colors=[ft.colors.BLACK,ft.colors.BLACK87, ft.colors.with_opacity(0.8,ft.colors.BLUE_800),ft.colors.BLACK87,ft.colors.BLACK],
        ),
        expand=True,
        padding=10,
        margin=0
    )



        # Resim içeren Container
    image_container = ft.Container(
        content=None,  # İçeriği yok
        image_src="./images/SbmBot_simple.png",  # Arka plan resmi URL'si
        padding=0,
        bgcolor=ft.colors.BLACK,
        margin=0
    )


        # İki Container'ı üst üste yerleştirmek için Stack kullanın
    stack = ft.Stack(
        controls=[
            image_container,
            gradient_container
        ],
        expand=True,

    )

    page.add(stack)

ft.app(target=main) 
