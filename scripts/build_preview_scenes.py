"""Original vector placeholders for design review. No external/official game assets."""
from pathlib import Path

def box(x,y,w,h,d,front,top,side):
    return f'<path d="M{x},{y}l{d},{-d}h{w}l{-d},{d}z" fill="{top}"/><path d="M{x+w},{y}l{d},{-d}v{h}l{-d},{d}z" fill="{side}"/><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="2" fill="{front}"/>'

def person(coat):
    return box(73,81,23,31,9,coat,'#d1e5db','#254958')+box(98,84,15,28,7,coat,'#bdd9ce','#254958')+box(75,112,12,24,7,'#263c52','#40627a','#17283b')+box(97,112,12,24,7,'#263c52','#40627a','#17283b')+box(63,85,11,24,7,'#edbb8d','#ffd9aa','#b17d60')+box(110,85,11,24,7,'#edbb8d','#ffd9aa','#b17d60')+box(71,43,37,32,10,'#edbb8d','#ffdbab','#b17d60')+'<path d="M71 43l10-10h37v13l-10 10V43H83v10H71z" fill="#67463f"/><rect x="81" y="57" width="5" height="6" rx="2" fill="#263647"/><rect x="98" y="57" width="5" height="6" rx="2" fill="#263647"/><path d="M88 69h9" stroke="#9c6154" stroke-width="2" stroke-linecap="round"/>'

equipment={
'fight':'<g transform="rotate(28 131 83)"><path d="M126 40l6-13 6 13v45h-12z" fill="#d9f6ed"/><path d="M132 28v57" stroke="#84b9bc" stroke-width="3"/><path d="M119 86h26" stroke="#f4c45e" stroke-width="6"/><path d="M132 89v18" stroke="#6e483f" stroke-width="7"/></g>',
'defend':'<path d="M117 78l24-8 22 8v32l-22 18-24-18z" fill="#629bcb" stroke="#c4e5e0" stroke-width="5"/><path d="M141 74v49m-20-28h39" stroke="#d8e8e5" stroke-width="5"/>',
'gather':box(131,111,30,25,12,'#64788a','#91a4a9','#3d4e65')+'<path d="M122 107l28-53" stroke="#b98458" stroke-width="8"/><path d="M127 54q21-10 37 11l-16-5-13 4z" fill="#b5dfdc"/>',
'build':box(120,91,42,45,14,'#b7855d','#d5af75','#805d55')+'<path d="M113 91l29-33 38 24-18 9-23-20-19 26z" fill="#e39567"/><rect x="136" y="112" width="15" height="24" fill="#3c5761"/><path d="M118 100h36m-36 12h13" stroke="#e4bb86" stroke-width="3"/>',
'survive':'<path d="M132 136l13-29 13 29" fill="#e78245"/><path d="M139 134l7-14 7 14" fill="#ffdc70"/><path d="M125 100h42l-6 23h-29z" fill="#526b77" stroke="#b6d2cb" stroke-width="3"/><path d="M140 92q-10-7 0-15m13 16q-10-7 0-15" stroke="#d7f0d3" opacity=".7" fill="none" stroke-width="3"/>',
'farm':'<path d="M126 136V94m15 42V86m16 50V98" stroke="#c9c867" stroke-width="4"/><path d="M126 107l-10-12m10 4l9-12m6 13l-9-14m9 6l10-14m6 34l-9-12m9 5l10-11" stroke="#e6d488" stroke-width="6" stroke-linecap="round"/>',
'explore':'<path d="M115 88l17-6 18 7 18-7v40l-18 7-18-8-17 7z" fill="#e3d4a0"/><path d="M132 84v36m18-30v38" stroke="#b5a679" stroke-width="2"/><path d="M126 110l10-10 14 10 11-11" stroke="#648c78" stroke-width="3" fill="none"/>',
'boss':box(130,87,28,37,10,'#7d6f98','#b5a0c3','#53476d')+box(130,63,30,22,10,'#8a7aa4','#b5a0c3','#53476d')+'<path d="M136 72h7m7 0h7" stroke="#ffcb77" stroke-width="4"/><path d="M131 64l-6-12m33 7l9-11" stroke="#a894b8" stroke-width="6"/>',
'skills':'<path d="M143 53l17 27-17 30-17-30z" fill="#a8a0f5"/><path d="M143 53v57l17-30z" fill="#786dc0"/><path d="M124 50l-5-5m46 8l5-5m-27-10v-8m-19 87l-6 5" stroke="#dccbfc" stroke-width="3"/>',
'workshop':box(120,104,42,10,10,'#b18357','#e1b982','#7e5c48')+box(123,115,7,22,4,'#8f6d50','#b89467','#624f41')+box(155,115,7,22,4,'#8f6d50','#b89467','#624f41')+'<path d="M135 102l17-27" stroke="#bd925d" stroke-width="5"/><path d="M144 74l13-3 7 12-14 4z" fill="#acccd0"/>'
}
colors=['#71b5be','#6c9bbb','#96b69a','#bc9d70','#d49e7b','#9eb974','#85b0b9','#b09bc8','#aa9bda','#b8a379']
root=Path(__file__).resolve().parents[1]/'assets/preview';root.mkdir(parents=True,exist_ok=True)
for (key,scene),color in zip(equipment.items(),colors):
 svg='<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 210 166"><ellipse cx="109" cy="140" rx="74" ry="14" fill="#081f2a" opacity=".35"/>'+box(39,136,132,7,13,'#567467','#8ba68a','#385357')+person(color)+scene+'<circle cx="46" cy="47" r="2" fill="#e6d29b"/><circle cx="170" cy="39" r="3" fill="#e6d29b" opacity=".6"/></svg>'
 (root/(key+'.svg')).write_text(svg+'\n')
