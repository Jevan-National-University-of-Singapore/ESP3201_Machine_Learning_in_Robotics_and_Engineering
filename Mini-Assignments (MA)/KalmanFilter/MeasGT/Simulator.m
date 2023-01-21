function Simulator(xErrStdv,yErrStdv)

para.st=1;
para.T=1;
para.xErr=xErrStdv;
para.yErr=yErrStdv;

% 1) get scenario
tg=DefineTg(para.st);

% 2) generate ground truth
gTruth=Trajectory(tg,para);

% 3) generate EO measurments
msg=GetMeas(gTruth,para);

% 5) write to file
fn='MeasGT';
fid = fopen(fn,'w');
for i=1:size(msg,1)
    fprintf(fid,'%5.0f,%8.2f,%8.2f,%8.2f,%8.2f,\r\n',...
        msg(i,1),msg(i,2),msg(i,3),msg(i,4),msg(i,4));
end
fclose(fid);
end
%==========================================================================
function tg=DefineTg(st)
% target information
rg=500;
bg=125*pi/180;
sp=12.5;
hd=-100*pi/180;
tg(1).t0=st;
tg(1).x0=rg*sin(bg);
tg(1).y0=rg*cos(bg);
tg(1).xd=sp*sin(hd);
tg(1).yd=sp*cos(hd);
tg(1).mv(1)=0; %'CV';
tg(1).dur(1)=30;

end
%==========================================================================
function tgM=Trajectory(tg,para)
for i=1:length(tg)
    tgi=tg(i);
    x=tgi.x0;
    y=tgi.y0;
    xd=tgi.xd;
    yd=tgi.yd;
    tgMi.t=tgi.t0;
    tgMi.x=[x y 50 xd yd 0]';
    for j=1:length(tgi.mv)
        for k=1:tgi.dur(j)/para.T
            if tgi.mv(j)==0
                x=x+xd*para.T;
                y=y+yd*para.T;
            elseif tgi.mv(j)==1
                hd=atan2(xd,yd);
                sp=norm([xd,yd]);
                x=x+(sp*para.T+0.5*tgi.ac(j)*para.T*para.T)*sin(hd);
                y=y+(sp*para.T+0.5*tgi.ac(j)*para.T*para.T)*cos(hd);
                sp=sp+tgi.ac(j)*para.T;
                xd=sp*sin(hd);
                yd=sp*cos(hd);
            elseif tgi.mv(j)==2
                hd=atan2(xd,yd);
                sp=norm([xd,yd]);
                hd=hd+tgi.tr(j)*para.T;
                xd=sp*sin(hd);
                yd=sp*cos(hd);
                x=x+xd*para.T; % approximate
                y=y+yd*para.T; % approximate
            end
            ii=length(tgMi.t)+1;
            tgMi.t(ii)=tgMi.t(end)+para.T;
            tgMi.x(:,ii)=[x y 50 xd yd 0]';
        end
    end
    tgM(i).t=tgMi.t;
    tgM(i).x=tgMi.x;
end
end
%==========================================================================
function msg=GetMeas(gTruth,para)
msg=[];
for i=1:length(gTruth)
    gti=gTruth(i);
    for detT=gti.t(1):para.T.t(end)
        ii=find(abs(gti.t-detT)<0.005);
        tgX=gti.x(1:3,ii);
        tgV=gti.x(4:6,ii);
        x=norm(tgX)+para.xErr*randn(1);
        y=norm(tgX)+para.yErr*randn(1);
        m1=[detT tgX(1) tgX(2) x y];
        msg=[msg; m1];
    end
end
end
%==========================================================================

%==========================================================================
function PlotGT(gTruth,para)
figure(1);
hold on;
for i=1:size(para.EOpos,2)
    x=para.EOpos(:,i);
    plot3(x(1),x(2),x(3),'g*');
    ang1=(para.EOypr(1,i)-para.EOfovx/2)*pi/180;
    ang2=(para.EOypr(1,i)+para.EOfovx/2)*pi/180;
    x1(1)=x(1)+1000*sin(ang1);
    x1(2)=x(2)+1000*cos(ang1);
    x2(1)=x(1)+1000*sin(ang2);
    x2(2)=x(2)+1000*cos(ang2);
    x1(3)=x(3);
    x2(3)=x(3);
    plot3([x1(1) x(1),x2(1)],[x1(2) x(2),x2(2)],[x1(3) x(3),x2(3)],'-g');
end

for i=1:length(gTruth)
    plot3(gTruth(i).x(1,:),gTruth(i).x(2,:),gTruth(i).x(3,:),'.-');
end

end