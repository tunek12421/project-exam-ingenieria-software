from PIL import Image, ImageDraw, ImageFont
import subprocess

def run_command(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd='/home/tunek/Descargas/DOCUMENTACION/project-exam')
    return result.stdout + result.stderr

def text_to_image(text, filename, title=""):
    lines = text.strip().split('\n')
    font_size = 14
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", font_size)
        title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf", 16)
    except:
        font = ImageFont.load_default()
        title_font = font

    line_height = font_size + 6
    padding = 20
    title_space = 40 if title else 0
    width = max(len(line) for line in lines) * 9 + padding * 2
    width = max(width, 600)
    height = len(lines) * line_height + padding * 2 + title_space

    img = Image.new('RGB', (width, height), color=(30, 30, 30))
    draw = ImageDraw.Draw(img)

    if title:
        draw.text((padding, padding - 5), f"$ {title}", fill=(130, 230, 130), font=title_font)

    y = padding + title_space
    for line in lines:
        if 'PASSED' in line:
            color = (80, 200, 80)
        elif 'FAILED' in line:
            color = (230, 80, 80)
        elif 'passed' in line:
            color = (80, 230, 80)
        elif '=====' in line:
            color = (180, 180, 180)
        elif 'examen-' in line or 'commit' in line:
            color = (230, 200, 80)
        elif 'Container' in line or 'Started' in line:
            color = (100, 180, 230)
        else:
            color = (210, 210, 210)
        draw.text((padding, y), line, fill=color, font=font)
        y += line_height

    img.save(filename)
    print(f'Generada: {filename}')

out_dir = '/home/tunek/Descargas/DOCUMENTACION/project-exam/docs/capturas'

# 1. Tests
test_output = run_command('python3 -m pytest -v 2>&1')
text_to_image(test_output, f'{out_dir}/tests.png', 'python3 -m pytest -v')

# 2. Git log
git_output = run_command('git log --oneline --decorate')
text_to_image(git_output, f'{out_dir}/git_log.png', 'git log --oneline')

# 3. Git branch
branch_output = run_command('git branch -a')
text_to_image(branch_output, f'{out_dir}/git_branch.png', 'git branch -a')

# 4. Docker
docker_output = run_command('docker compose ps 2>&1')
text_to_image(docker_output, f'{out_dir}/docker_ps.png', 'docker compose ps')

# 5. Estructura
tree_output = run_command("find . -type f -not -path './.git/*' -not -path './__pycache__/*' -not -path './.pytest_cache/*' -not -name '*.pyc' -not -name '*.db' -not -name '.~lock*' | sort | head -40")
text_to_image(tree_output, f'{out_dir}/estructura.png', 'Estructura del proyecto')
