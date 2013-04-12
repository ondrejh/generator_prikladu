% vycisteni workspace
close all
clear all

jmeno_souboru = 'priklady.html'; %nazev souboru s vystupem
celkem_prikladu = int32(34); %celkovy pocet prikladu (s danym stylem odpovida 1 strance)
prikladu_na_radek = int32(2); %nemenit! (muselo by se to spravit ve stylu)

%zarovnani poctu prikladu
if idivide(celkem_prikladu,prikladu_na_radek)*prikladu_na_radek~=celkem_prikladu
	celkem_prikladu = idivide(celkem_prikladu,prikladu_na_radek,'ceil')*prikladu_na_radek;
end %if

priklady = [];
pocet = 0;

while (pocet<celkem_prikladu)

	%vygenerovani prikladu
	a = round(rand(1)*20); %a
	z = round(rand(1)); %znamenko (0 ~ +, 1 ~ -)
	b = round(rand(1)*20); %b
	v = 1; %platnost

	%overeni platnosti prikladu
	if ((z==1)&&(b>=a))
		v = 0;
	end %pri odecitani nesmi byt b>=a
	if ((z==0)&&((a+b)>20))
		v = 0;
	end %soucet nesmi byt vic nez 20
	if ((z==1)&&(b>10))
		v = 0; 
	end %pri odecitani nesmi byt b>10
	if ((a==0)||(b==0)) 
		v = 0; 
	end %a nebo b nesmi byt 0

	%pridani do seznamu
	if (v==1)
		%test jestli se priklad neopakuje
		p = 0;
		for i=1:pocet
			if ((a==priklady(i,1))&&(z==priklady(i,2))&&(b==priklady(i,3))) 
				p=1;
			end %if
		end %for

		%pridani prikladu na konec seznamu
		if (p==0)
			priklady(pocet+1,:)=[a,z,b];
			pocet=pocet+1;
		end %if
	end %if

end %while


%zobrazeni prikladu
pocet
priklady

%vygenerovani vystupu
fid = fopen (jmeno_souboru, 'w');

%hlavicka
fprintf(fid,['<!DOCTYPE HTML>\n' ...
			 '<html>\n' ...
			 '<head>\n' ...
			 '<meta http-equiv=\"Content-Type\" content=\"text/html; charset=UTF-8\" />\n' ...
			 '<title>Generator prikladu</title>\n' ...
			 '<link rel=\"stylesheet\" type=\"text/css\" href=\"style.css\" media=\"screen\" />\n'...
			 '<link rel=\"stylesheet\" href=\"style.css\" media=\"print\" />\n' ...
			 '<link rel=\"shortcut icon\" href=\"calculator.ico\" />\n' ...
			 '</head>\n' ...
			 '<body>\n' ...
			 '<section id=main>\n' ...
			 '<article><p><table>\n']);

%priklady
for i=1:pocet
	if (i-idivide(i,prikladu_na_radek)*prikladu_na_radek==1) 
		fprintf(fid,' <tr>'); 
	end %if
	a=priklady(i,1);
	z='+';
	if priklady(i,2)==1 
		z='-';
	end %if
	b=priklady(i,3);
	fprintf(fid,'<td>%d</td><td>%c</td><td>%d</td><td>=</td>&nbsp;<td></td>',a,z,b);
	if (i-idivide(i,prikladu_na_radek)*prikladu_na_radek==0) 
		fprintf(fid,'</tr>\n'); 
	end %if
end %for

%zapati
fprintf(fid,'</table></p></article>\n');

fclose (fid);