import os, subprocess, shutil
r = r"C:\Users\Luis\calude"
desk = r"C:\Users\Luis\Desktop\Papás Primerizos"
V = {
 1: ("Estoy bien cuando no lo estás", ["SI TU HIJO", "TE NOTA TRISTE,", "NO LE DIGAS", "«ESTOY BIEN»"], 1),
 2: ("Si estás separado no hables mal del otro", ["NO HABLES MAL", "DEL OTRO FRENTE", "A TU HIJO"], 1),
 3: ("Cómo se dice", ["NO LE PREGUNTES", "A TU HIJO", "«¿CÓMO SE DICE?»"], 1),
 4: ("Si tu hijo te invita a bailar baila", ["SI TU HIJO", "TE INVITA A", "BAILAR, BAILA"], 1),
 5: ("Si no quiere el abrigo", ["SI TU HIJO NO", "QUIERE EL ABRIGO,", "DÉJALO SENTIR", "UN POCO DE FRÍO"], 1),
 6: ("No lo apures a dejar el pañal", ["NO APURES", "A TU HIJO", "CON EL PAÑAL"], 1),
}
Y = "&H0000E6FF&"  # amarillo
for n, (nom, lines, img) in V.items():
    d = f"{r}\\papas{n}"
    if n == 1:
        src = f"{d}\\imagenes\\img_{img:02d}.jpg"
    else:
        src = f"{d}\\imagenes\\img_{img:02d}.jpg"
    size = int(min(215, 1010 / (max(len(l) for l in lines) * 0.36)))
    txt = r"\N".join(lines[:-1]) + r"\N{\1c" + Y + "&}" + lines[-1]
    ass = f"""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 2

[V4+ Styles]
Format: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,BackColour,Bold,Italic,Underline,StrikeOut,ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding
Style: T,Baloo 2 ExtraBold,{size},&H00FFFFFF,&H00FFFFFF,&H00000000,&H90000000,0,0,0,0,100,100,0,0,1,16,6,2,30,30,380,1

[Events]
Format: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text
Dialogue: 0,0:00:00.00,0:00:05.00,T,,0,0,0,,{txt}
"""
    open(f"{d}\\min.ass", "w", encoding="utf-8").write(ass)
    # sin texto (respaldo) y con titular
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", src, "-vf", "scale=1080:1920:flags=lanczos", "-q:v", "2", f"{d}\\miniatura_sin_texto.jpg"], check=True)
    # degradado oscuro arriba para que el titular se lea
    vf = "scale=1080:1920:flags=lanczos,subtitles=min.ass:fontsdir=fuentes"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", src, "-vf", vf, "-frames:v", "1", "-q:v", "2", f"{d}\\miniatura.jpg"], check=True, cwd=d)
    dst = os.path.join(desk, nom)
    shutil.copy(f"{d}\\miniatura.jpg", os.path.join(dst, "miniatura.jpg"))
    print("OK", n, nom)



