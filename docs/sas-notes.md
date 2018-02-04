## Determine Runtime Environment
```sas
%macro check;
 
  %if %symexist(_clientapp) %then %do;
   %if &_clientapp = SAS Studio %then %do;
    %put Running SAS Studio;
   %end;
   %else %if &_clientapp= 'SAS Enterprise Guide' %then %do;
    %put Running SAS Enterprise Guide; 
   %end;
  %end;
 
  %else %if %index(&sysprocessname,DMS) %then %do;
    %put Running in Display Manager;
  %end;
  %else %if %index(&sysprocessname,Program) %then %do;
     %let prog=%qscan(%superq(sysprocessname),2,%str( ));
     %put Running in batch and the program running is &prog;
  %end;
 
  %mend check;
 %check
```
