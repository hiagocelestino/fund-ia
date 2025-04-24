from moviepy import TextClip, concatenate_videoclips


def generate_gif(input: list[str]):
    font_path = "C:/Windows/Fonts/arial.ttf"

    clips = [
        TextClip(text=texto, font=font_path, color='white', bg_color='black', size=(400, 400))
        .with_duration(0.7)
        for texto in input
    ]

    video = concatenate_videoclips(clips)
    video.write_gif("./executions.gif", fps=10)
