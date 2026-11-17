from pathlib import Path
import re, html, fitz

root = Path(__file__).resolve().parent
doc = fitz.open(root / 'Final_DeMo.pdf')
blocks = [[b[4] for b in page.get_text('blocks')] for page in doc]

def clean(s):
    s = re.sub(r'-\n(?=[a-z])', '', s)
    s = re.sub(r'\s*\n\s*', ' ', s).strip()
    s = re.sub(r'([𝑡𝑖𝑘𝑚𝐺𝑑∗])(?=[a-zA-Z])', r'\1 ', s)
    return s

parts = []
def para(page, index):
    parts.append('<p>' + html.escape(clean(blocks[page-1][index])) + '</p>')
def heading(n, title, anchor):
    parts.append(f'<section id="{anchor}"><h2>{title}</h2>')
def end(): parts.append('</section>')
def eq(n, expression):
    parts.append(f'<div class="equation"><span class="math" data-tex="{html.escape(expression, quote=True)}">{html.escape(expression)}</span><span class="number">({n})</span></div>')

parts.append('<section id="abstract"><h2>Abstract</h2>')
para(1,5); end()
heading(1,'Stochastic gradient descent with momentum','momentum')
para(1,7); para(1,8)
eq(1,r'\mathbf{x}_{t+1}:=\mathbf{x}_t-\eta\nabla\ell(\mathbf{x}_t)')
para(1,10)
eq(2,r'\Delta\mathbf{x}_t:=\alpha\Delta\mathbf{x}_{t-1}-\eta\nabla\ell(\mathbf{x}_t)')
eq(3,r'\mathbf{x}_{t+1}:=\mathbf{x}_t+\Delta\mathbf{x}_t')
para(2,1); end()
heading(2,'The unproven conjectures','conjectures')
for i in [3,4,5,6]: para(2,i)
end()
heading(3,'Separating components','components')
para(3,2); para(3,3)
eq(4,r'\Sigma=\operatorname{Cov}(\mathbf X)=\mathbb E\left[(\mathbf X-\mathbb E[\mathbf X])(\mathbf X-\mathbb E[\mathbf X])^T\right]')
para(3,8); para(3,9)
eq(5,r'\Sigma\mathbf v_i=\lambda_i\mathbf v_i,\qquad i=1,\ldots,d')
para(3,11)
eq(6,r'\mathbf y_i=\mathbf v_i^\top\mathbf X,\qquad\operatorname{Var}(\mathbf y_i)=\lambda_i')
para(3,14); para(3,15)
tail = blocks[2][16] + blocks[2][17] + blocks[2][18] + blocks[3][1]
tail = tail.replace('˜𝑚freq\n𝑡\nand the indices tensor ˜𝑚ampl\n𝑡\n.', 'm̃ᶠʳᵉᵠₜ and the indices tensor m̃ᵃᵐᵖˡₜ.')
parts.append('<p>'+html.escape(clean(tail))+'</p>')
eq(7,r'\widetilde m_t^{\mathrm{freq}},\widetilde m_t^{\mathrm{ampl}}=p(\mathbf m_t,s,k)')
para(4,5)
eq(8,r'\mathbf q_t^*=p^{-1}(\widetilde m_t^{\mathrm{freq}},\widetilde m_t^{\mathrm{ampl}})')
end()
heading(4,'DeMo; the algorithm','algorithm')
para(4,12)
eq(9,r'\widetilde{\mathbf g}_t=\nabla\ell(\mathbf x_t;\mathcal B_t)\in\mathbb R^d')
para(4,14)
eq(10,r'\mathbf m_t\leftarrow\beta\mathbf m_t+\widetilde{\mathbf g}_t,\qquad\mathbf m_t\in\mathbb R^d')
para(4,16)
eq(11,r'\mathbf q_t^*=p(\mathbf m_t,s,k)\in\mathbb R^d')
para(4,19)
eq(12,r'\mathbf m_{t+1}=\mathbf m_t-\mathbf q_t^*,\qquad\mathbf m_{t+1}\in\mathbb R^d')
para(4,22)
eq(13,r'\mathbf Q_t=\frac1G\sum_{g=1}^{G}\mathbf q_t^{*(g)}\in\mathbb R^d')
parts.append('<p>'+html.escape(clean((blocks[3][29]+blocks[3][30]).replace('q∗\n𝑡', 'q∗ₜ')))+'</p>')
eq(14,r'\mathbf x_{t+1}=\mathbf x_t-\eta\mathbf Q_t,\qquad\mathbf x_{t+1}\in\mathbb R^d')
para(4,32); end()
heading(5,'Conclusion','conclusion'); para(5,2); end()
parts.append('<section id="references"><h2>References</h2><ol>')
for indices in [[4,5],[6,7],[8],[9],[10],[11,12],[13,14],[15,16]]:
    text = clean(''.join(blocks[4][i] for i in indices))
    text = re.sub(r'^\[\d+\]\s*','',text)
    parts.append('<li>'+html.escape(text)+'</li>')
parts.append('</ol></section>')

template = (root/'template.html').read_text(encoding='utf-8')
(root/'index.html').write_text(template.replace('<!-- ARTICLE -->','\n'.join(parts)),encoding='utf-8')
print('Generated index.html: 5 sections, 14 equations, 8 references.')
