import csv
import os

import flet as ft
from flet.core.types import ScrollMode

light_pink= "#ffcdb2"
pink=       "#ffb4a2"
not_pink=   "#e5989b"
grey_pink=  "#b5838d"
grey=       "#6d6875"

basis_ordner = os.path.dirname(__file__)
datei = os.path.join(basis_ordner, "Maschen.csv")


class AnzeigeButton(ft.TextField):
    def __init__(self, text,):
        super().__init__(
            value= text,
            expand=False,
            border_width=0,
            bgcolor=not_pink,
            color=grey,
            border_radius=20,
            adaptive=True,
            multiline=True,
            read_only=True,
            text_size=16
            )

def main(page: ft.Page):
    page.title="Maschenanschläge fürs Hausschuhe stricken"
    page.bgcolor=light_pink
    page.scroll = ft.ScrollMode.ALWAYS
    page.window_full_screen = True
    page.adaptive = True

    def schrift_anpassen(e):
        schriftgröße = 8 if page.window.width < 500 else 16
        überschriftgröße = 10 if page.window.width < 500 else 20

        for btn in [
            groesse_button,
            maschenanschlag_button,
            offengestricktereihen_button,
            geschlossenerunden_button
        ]:
            btn.style = ft.ButtonStyle(
                text_style=ft.TextStyle(size=schriftgröße)
            )

        headText.size = überschriftgröße
        page.update()

    page.on_resize=schrift_anpassen

    def laden():
        global daten
        with open(datei, mode='r', encoding='utf-8') as csv_datei:
            csv_leser = csv.DictReader(csv_datei)
            daten = list(csv_leser)
        page.update()

    def personen_bestimmen():
        global personen
        personen = [eintrag['Groesse'] for eintrag in daten[23:]]

    laden()
    personen_bestimmen()

    global ausgewahlter_eintrag
    ausgewahlter_eintrag= None

    def finde_eintrag(eingabe):
        for eintrag in daten:
            if str(eintrag['Groesse']) == str(eingabe):
                return eintrag
        return None

    def standard_text(key):
        if not ausgewahlter_eintrag:
            return "bitte Auswahl treffen"
        else:
            return ausgewahlter_eintrag.get(key, "keine Wert")

    groesse_button = AnzeigeButton(text=f"Größe/Name:\n{standard_text('Groesse')}")
    maschenanschlag_button = AnzeigeButton(text=f"Maschenanschlag:\n{standard_text('Maschenanschlag')}")
    offengestricktereihen_button = AnzeigeButton(
        text=f"Offen geschrickte Reihen:\n{standard_text('offen gestrickte Reihen ab Anschlag')}"
    )
    geschlossenerunden_button = AnzeigeButton(text=f"Geschlossene Runden:\n{standard_text('geschlossene Runden')}")

    groesse_textfeld = ft.TextField(
        label=f"Größe/Name:\ {standard_text('Groesse')}", bgcolor=not_pink, border_radius=20,
        adaptive=True, border_width=0, label_style=ft.TextStyle(color=grey))
    maschenanschlag_textfeld = ft.TextField(label=f"Maschenanschlag: {standard_text('Maschenanschlag')}",
                                            bgcolor=not_pink, border_radius=20, adaptive=True, border_width=0,
                                            label_style=ft.TextStyle(color=grey))
    offengestricktereihen_textfeld = ft.TextField(
        bgcolor=not_pink, border_radius=20, adaptive=True, border_width=0, label_style=ft.TextStyle(color=grey),
        label=f"Offen geschrickte Reihen: {standard_text('offen gestrickte Reihen ab Anschlag')}"
    )
    geschlossenerunden_textfeld = ft.TextField(
        bgcolor=not_pink, border_radius=20, adaptive=True, border_width=0, label_style=ft.TextStyle(color=grey),
        label=f"Geschlossene Runden: {standard_text('geschlossene Runden')}")

    def aktualisiere_buttons():
        groesse_button.value = f"Größe/Name: {standard_text('Groesse')}"
        maschenanschlag_button.value = f"Maschenanschlag: {standard_text('Maschenanschlag')}"
        offengestricktereihen_button.value = f"Offen geschrickte Reihen: {standard_text('offen gestrickte Reihen ab Anschlag')}"
        geschlossenerunden_button.value = f"Geschlossene Runden: {standard_text('geschlossene Runden')}"

        groesse_textfeld.label = f"Groesse/Name: {standard_text('Groesse')}"
        maschenanschlag_textfeld.label = f"Maschenanschlag: {standard_text('Maschenanschlag')}"
        offengestricktereihen_textfeld.label = f"Offen geschrickte Reihen: {standard_text('offen gestrickte Reihen ab Anschlag')}"
        geschlossenerunden_textfeld.label = f"Geschlossene Runden: {standard_text('geschlossene Runden')}"
        page.update()

    def tabelle_umschalten(e):
        tabelle.visible = not tabelle.visible
        tabelle_button.text = "Tabelle verbergen" if tabelle.visible else "Gesamte Tabelle anzeigen"
        page.update()

    def aktualisiere_tabelle():
        # Neue Zeilen basierend auf aktuellen 'daten'
        neue_zeilen = [
            ft.DataRow(
                cells=[
                    ft.DataCell(
                        ft.Text(eintrag[spalte], text_align=ft.TextAlign.CENTER)
                    ) for spalte in spalten_namen
                ],
                color=not_pink if i % 2 == 1 else pink
            )
            for i, eintrag in enumerate(daten)
        ]

        # Tabelle aktualisieren
        tabelle.rows = neue_zeilen
        page.update()

    def bearbeiten_umschalten(e):
        auswahl_anzeigen.visible = not auswahl_anzeigen.visible
        auswahl_ändern.visible = not auswahl_ändern.visible
        groessenwerte_bearbeiten.text = "Zurück" if auswahl_ändern.visible else "Werte anpassen / hinzufügen"
        groessenwerte_bearbeiten.icon = ft.Icons.WARNING_ROUNDED if auswahl_ändern.visible else ft.Icons.EDIT
        groessenwerte_bearbeiten.icon_color = ft.Colors.RED if auswahl_ändern.visible else ft.Colors.DEEP_ORANGE
        page.update()

    def sortierschluessel(eintrag):
        groesse = eintrag["Groesse"]
        try:
            # Wenn groesse wie eine Zahl aussieht, z. B. "38"
            return (0, int(groesse))
        except ValueError:
            # Wenn groesse kein int ist, z. B. "Max"
            return (1, groesse.lower())  # Namen alphabetisch sortieren

    daten.sort(key=sortierschluessel)


    def speichern(e):
        # Alte Werte zwischenspeichern
        alte_groesse = ausgewahlter_eintrag["Groesse"]
        alter_maschenanschlag = ausgewahlter_eintrag["Maschenanschlag"]
        alte_offen_reihen = ausgewahlter_eintrag["offen gestrickte Reihen ab Anschlag"]
        alte_geschlossene = ausgewahlter_eintrag["geschlossene Runden"]

        # Neue Werte: entweder das, was der Nutzer eingegeben hat,
        # oder – wenn das Feld leer ist – den alten Wert
        neue_groesse = groesse_textfeld.value or alte_groesse
        neuer_maschenanschlag = maschenanschlag_textfeld.value or alter_maschenanschlag
        neue_offen_reihen = offengestricktereihen_textfeld.value or alte_offen_reihen
        neue_geschlossene_runden = geschlossenerunden_textfeld.value or alte_geschlossene

        # Das neue Dictionary
        neuer_eintrag = {
            "Groesse": neue_groesse,
            "Maschenanschlag": neuer_maschenanschlag,
            "offen gestrickte Reihen ab Anschlag": neue_offen_reihen,
            "geschlossene Runden": neue_geschlossene_runden
        }

        # Alten Eintrag (nach alter Größe) entfernen und neuen einfügen
        daten[:] = [d for d in daten if d["Groesse"] != alte_groesse]
        daten.append(neuer_eintrag)

        # Optional: wieder sortieren
        daten.sort(key=sortierschluessel)

        # CSV neu schreiben
        with open(datei, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=neuer_eintrag.keys(), delimiter=",")
            writer.writeheader()
            writer.writerows(daten)

        bearbeiten_umschalten(None)
        for feld in [groesse_textfeld, maschenanschlag_textfeld,
                     offengestricktereihen_textfeld, geschlossenerunden_textfeld]:
            feld.value = ""

        aktualisiere_tabelle()
        verarbeite_auswahl()

        # UI aktualisieren
        page.update()


    dropdown = ft.Dropdown(
            label="Name auswählen",
            label_style=ft.TextStyle(color="black"),
            hint_text=".....",
            fill_color=pink,
            options=[ft.dropdown.Option(person) for person in personen],
            on_change=lambda e: dropdown_geaendert()
        )

    eingabe_textfeld = ft.TextField(label="Größe 27 - 49...",color="black" ,bgcolor=pink,
                                    label_style=ft.TextStyle(color="black"), on_submit=lambda e: textfeld_geaendert())
    eingabe_button = ft.FilledButton(text="Auswählen", icon="favorite", color="black",
                                     bgcolor=not_pink, icon_color="red", on_click=lambda e: textfeld_geaendert())

    def dropdown_geaendert():
        eingabe_textfeld.value = ""
        verarbeite_auswahl()
        page.update()

    def textfeld_geaendert():
        dropdown.value = None
        verarbeite_auswahl()
        page.update()

    def verarbeite_auswahl():
        global ausgewahlter_eintrag
        eingabe = dropdown.value or eingabe_textfeld.value
        eintrag = finde_eintrag(eingabe)
        if eintrag:
            ausgewahlter_eintrag = eintrag
            aktualisiere_buttons()

    headText= ft.Container(
        content=ft.Text(value="Wähle rechts einen Namen oder lasse dir rechts eine Schuhgröße anzeigen",
                    size=20,
                    text_align=ft.TextAlign.CENTER,
                    style=ft.TextStyle(
                        weight=ft.FontWeight.BOLD, color=grey
                    )),
        bgcolor=pink,
        padding=10,
        border_radius=20,
        margin=10,
        alignment= ft.alignment.center,
    )

    schuhgroesse_eingabe = ft.Column(
        controls=[eingabe_textfeld,
                  eingabe_button
                  ])

    select_row = ft.Container(
        content=ft.Row(
        controls=[
            ft.Container(
                alignment=ft.alignment.center,
            content=ft.Column(controls=[dropdown, ft.Container(height=33, opacity=0, expand=True)]),),
            ft.Container(schuhgroesse_eingabe),],
        alignment=ft.MainAxisAlignment.CENTER
    ),margin=ft.margin.only(top=20),alignment=ft.alignment.center)

    auswahl_anzeigen = ft.Container(
        visible=True,
        content=ft.Row(
        controls=[ft.Container(
            ft.Column(
                controls=[
                    ft.Container(groesse_button, padding=5),
                    ft.Container(maschenanschlag_button, padding=5),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                wrap=True
            ), width=350),
            ft.Container(ft.Column(
                controls=[
                    ft.Container(offengestricktereihen_button, padding=5),
                    ft.Container(geschlossenerunden_button, padding=5),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                wrap=True
            ), width= 350),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
    ), margin=ft.margin.only(top=40), alignment=ft.alignment.center,expand=True,)

    auswahl_ändern = ft.Container(
        visible=False,
        content=ft.Row(
        controls=[ft.Container(
            ft.Column(
                controls=[
                    ft.Container(groesse_textfeld, padding=5),
                    ft.Container(maschenanschlag_textfeld, padding=5),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                wrap=True
            ), width=350),
            ft.Container(ft.Column(
                controls=[
                    ft.Container(offengestricktereihen_textfeld, padding=5),
                    ft.Container(geschlossenerunden_textfeld, padding=5),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                wrap=True
            ), width= 350),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
    ), margin=ft.margin.only(top=40), alignment=ft.alignment.center,expand=True)


    groessenwerte_bearbeiten = ft.ElevatedButton(
        on_click=bearbeiten_umschalten,
        text ="Werte anpassen / hinzufügen", icon=ft.Icons.EDIT, bgcolor=not_pink, icon_color=ft.Colors.DEEP_ORANGE,
        style=ft.ButtonStyle(color=grey,
                             text_style=ft.TextStyle(size=16, weight=ft.FontWeight.BOLD,),
                             ))
    speichern_button = ft.ElevatedButton(text="Anpassungen speichern",
                                         on_click=speichern,
                                         icon=ft.Icons.SAVE,
                                         bgcolor=not_pink,
                                         icon_color=ft.Colors.LIGHT_BLUE_ACCENT_200,
                                         style=ft.ButtonStyle(
                                             color=grey,
                                             text_style=ft.TextStyle(size=16, weight=ft.FontWeight.BOLD,),
                                         ))
    tabelle_button = ft.ElevatedButton(text="Gesamte Tabelle anzeigen", icon=ft.Icons.TABLE_ROWS, bgcolor=not_pink,
                                         icon_color=ft.Colors.BROWN, on_click=tabelle_umschalten,
                                         style=ft.ButtonStyle(
                                             color=grey,
                                         text_style=ft.TextStyle(size=16, weight=ft.FontWeight.BOLD)))
    tabelle_anzeigen = ft.Container(
        expand=True,
        content=tabelle_button)

    bearbeiten_row = ft.Container(
        expand=True,
        content=ft.Row(
        controls=[ft.Container(groessenwerte_bearbeiten, width=200), ft.Container(speichern_button, width=200)],
        alignment=ft.MainAxisAlignment.CENTER,
    ), margin=ft.margin.only(top=40))

    spalten_namen = daten[0].keys()

    spalten = [
        ft.DataColumn(ft.Text(spalte))
        for spalte in spalten_namen
    ]

    zeilen = [
        ft.DataRow(
            cells=[
                ft.DataCell(
                    ft.Text(eintrag[spalte], text_align=ft.TextAlign.CENTER)
                ) for spalte in spalten_namen
            ],
            color=not_pink if i % 2 == 1 else pink
        )
        for i, eintrag in enumerate(daten)
    ]



    tabelle = ft.DataTable(
        visible=False,
        columns=spalten,
        rows=zeilen,
        heading_row_color=grey_pink,
        border=ft.border.all(5,grey),
        border_radius=20,
        vertical_lines=ft.BorderSide(3,"grey"),
        horizontal_lines=ft.BorderSide(3,"grey"),
        show_checkbox_column=False
    )

    scrollbare_tabelle = ft.Column(
        controls=[
            tabelle,
        ],
        scroll=ScrollMode.ALWAYS,
        #height=600,
    )

    safe_area = ft.SafeArea(
            expand=True,
            top=True,
            bottom=False,
            content=
                ft.Container(
                bgcolor=light_pink,
                alignment=ft.alignment.top_center,
                content=ft.Column(
                    scroll=ScrollMode.ALWAYS,
                    #width=800,
                    controls=[headText, select_row, auswahl_anzeigen, auswahl_ändern, bearbeiten_row,tabelle_anzeigen, scrollbare_tabelle],
                    expand=True,
                    alignment=ft.MainAxisAlignment.START,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),expand=True,


                )
            )

    viewer = ft.InteractiveViewer(
        min_scale=0.5,  # Mindestmaßstab (hier 50% der Originalgröße)
        max_scale=3.0,  # Maximalmaßstab (300% der Originalgröße)
        scale_enabled=True,  # Aktiviert das Zoomen per Fingerbewegung
        pan_enabled=True,  # Aktiviert das Verschieben (Panning)
        content=safe_area,
    )

    page.add(viewer)


#ft.app(target=main)
#ft.app(target=main, view=ft.WEB_BROWSER, host="0.0.0.0", port=8550)
ft.app(target=main, view=ft.WEB_BROWSER)
