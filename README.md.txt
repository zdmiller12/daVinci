% Overleaf v2 uses pdfLaTeX compiler as default

%%% How I Manually Installed Packages (when necessary)
% 1. download from CTAN (or wherever)
% 2. unzip (if necessary)
% 3. using MikTeX Console application, open a console
% 4. run "latex packageName.ins"
% 5. copy directory and contents to C:\Users\zdmil\AppData\Local\Programs\MiKTeX 2.9\tex/latex/packageName
% 6. run Tasks > Refresh file name database
%%%

%%%%%
%%%%
%%%
%%
%     SOLUTION MANUAL

% for solution manual to be up-to-date, there are manual steps (probably Overleaf weirdness)
% 1. download the output*.sol.tex file from a mainText.tex compilation (& verify it's populated)
% 2. upload the file in STEA/Solution Manual/ as stea.sol.tex 
%      *MUST change from output.sol.tex, or the new output is used
% 3. in Menu, change Main Document to STEA/SolutionManual/mainSolutionManual.tex
% 4. compile, download
% 5. In Menu, change Main Document back to mainText.tex
%
% * compiling solutions.tex produces a blank output*.sol.tex file, which it imports, but is blank
%
%%
%%%
%%%%
%%%%%


Header from LaTeX Template
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% The Legrand Orange Book
% LaTeX Template
% Version 2.3 (8/8/17)
%
% This template has been downloaded from:
% http://www.LaTeXTemplates.com
%
% Original author:
% Mathias Legrand (legrand.mathias@gmail.com) with modifications by:
% Vel (vel@latextemplates.com)
%
% License:
% CC BY-NC-SA 3.0 (http://creativecommons.org/licenses/by-nc-sa/3.0/)
%
% Compiling this template:
% This template uses biber for its bibliography and makeindex for its index.
% When you first open the template, compile it from the command line with the 
% commands below to make sure your LaTeX distribution is configured correctly:
%
% 1) pdflatex main
% 2) makeindex main.idx -s StyleInd.ist
% 3) biber main
% 4) pdflatex main x 2
%
% After this, when you wish to update the bibliography/index use the appropriate
% command above and make sure to compile with pdflatex several times 
% afterwards to propagate your changes to the document.
%
% This template also uses a number of packages which may need to be
% updated to the newest versions for the template to compile. It is strongly
% recommended you update your LaTeX distribution if you have any
% compilation errors.
%
% Important note:
% Chapter heading images should have a 2:1 width:height ratio,
% e.g. 920px width and 460px height.
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%