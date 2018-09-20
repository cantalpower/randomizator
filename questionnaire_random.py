from random import randint,shuffle
from math import floor

def lecture (chemin):
	fichier=open(chemin,'r')
	noms =[]
	questions = []
	quest52 =[]
	for ligne in fichier:
		elem=ligne.split(',')
		if elem[0] != '' :
			noms.append(elem[0])
		if elem[1] != '' :
			questions.append(elem[1])
		if elem[2] != '' :quest52.append(elem[2])
	return (noms[1:],questions[1:],quest52[1:])

def randomiser(noms,questions):
	listequest=[]
	n= len(noms)
	q= len(questions)
	for quest in questions:
		aleat=[randint(0,n-1) for k in range(3)]
		for nbr in aleat:
			listequest.append(quest+' '+noms[nbr]+'?')
		
	return listequest
				
def preparer_questionnaire(liste,q52):
	shuffle(liste)
	questionnaires=[liste[k:k+8]+[q52[a] for a in [randint(0,len(q52)-1)for i in range(3)]] for k in range(int(len(liste)/8))]
	return questionnaires
	
def latexiser(questionnaire,numero):
	import os,glob,subprocess
	
	header = r'''%%%%%%%%
% Class
%%%%%%%%
\documentclass[utf8,a4paper,french,12pt,fleqn]{article}

%%%%%%%%%%%%%%%%%%%
% Package
%%%%%%%%%%%%%%%%%%%

%%%%%%%%%%
% Packages
%%%%%%%%%%
\usepackage[utf8]{inputenc}
%AMS
\usepackage{amsmath} % macros ams
\usepackage{amsfonts} % fonts ams
\usepackage{amssymb} % symboles ams

%Mise en page
\usepackage[top=2.5cm,bottom=2.5cm,left=2.5cm,right=2.5cm]{geometry} 
\usepackage{fancyhdr} % Entêtes et pieds de page

%Symboles mathematiques
\usepackage{latexsym}


\usepackage{Pstricks}
\usepackage{pst-grad}
\usepackage{pst-coil}
\usepackage{pst-blur}
\usepackage[tikz]{bclogo}

\newenvironment{Zapf}  {\fontfamily{pzc}\selectfont}{} % police "fantaisie" pour le mot FIN

%%%%%%%%%%%%%%%%%%%
% Mise en page
%%%%%%%%%%%%%%%%%%%

\parindent=0cm
%Entete et bas de page
\makeatletter
\let \ps@plain=\ps@fancy
\makeatother

\pagestyle{fancy}
\renewcommand{\headrulewidth}{.0pt} % largeur du filet de l’entête (0pt=pas de filet)
\fancyhead[L]{} % entête droite
%\fancyhead[R]{} % entête gauche
%\fancyhead[C]{} % entête centrée
\renewcommand{\footrulewidth}{.0pt} % largeur du filet de l’entête (0pt=pas de filet)
\fancyfoot[R]{2018-2019 } % entête droite
\fancyfoot[L]{MP} % entête gauche
\fancyfoot[C]{ } % entête centrée

\begin{document}

\begin{center}
\begin{Huge}
Devoir Maison $\text{n}^{\circ}$1 \\
\end{Huge}

\hspace{1cm}

\begin{Large}
\textsc{Nom} - Prénom
\end{Large}
\end{center}

\hspace{3cm}

\begin{bclogo}[logo=\bcbook]{Les Règles du jeu}
Quelques petits conseils ...
\end{bclogo}

\hspace{3cm}	'''
	
	footer = r'''\hspace{7cm}

		\begin{Zapf} \noindent \centerline{\fontsize{22}{22}\selectfont -- = BON COURAGE = -- } \end{Zapf}


\end{document}'''
	main= r''' '''
	
	for k in range(1,len(questionnaire)+1):
		main += r'''
		
{\large \textbf{Question '''+str(k)+ r''' :}} ''' + questionnaire[k-1] + r''' \\

\hspace{8cm} '''
	
	content = header + main + footer
	
	titre='questionnaire_'+str(numero)+'.tex'
	with open(titre,'w') as f:
		f.write(content)
	
	commandLine = subprocess.Popen(['pdflatex', titre])
	commandLine.communicate()
	
	os.unlink('questionnaire_'+str(numero)+'.aux')
	os.unlink('questionnaire_'+str(numero)+'.log')
	os.unlink('questionnaire_'+str(numero)+'.tex')
	
#noms=['zobidi '+str(k) for k in range(32)]
#questions=['quest '+str(k) for k in range(80)]
#q52=['q52 '+str(k) for k in range(20)]

noms,questions,q52= lecture('qcm.csv')
resultat=randomiser(noms,questions)
questionnaires=preparer_questionnaire(resultat,q52)
for k in range(len(questionnaires)):
#k=0
	latexiser(questionnaires[k],k)

