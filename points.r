studyId = "999"
dataFile0 = "points0.data"
dataFile7 = "points7.data"
dataFile14 = "points14.data"
dataFile21 = "points21.data"

goal = 1000
bounds = c(0,400)

targets = c(42,84,126,182,224)
goals = rep(goal, length(targets))


args = commandArgs(TRUE)
if(length(args) == 3){
   studyId = args[[1]]
   dataFile = args[[2]]
   target = args[[3]]
}

data0  = read.csv(dataFile0 ,header=FALSE,sep=",",stringsAsFactors=TRUE)
data7  = read.csv(dataFile7 ,header=FALSE,sep=",",stringsAsFactors=TRUE)
data14 = read.csv(dataFile14,header=FALSE,sep=",",stringsAsFactors=TRUE)
data21 = read.csv(dataFile21,header=FALSE,sep=",",stringsAsFactors=TRUE)

#data = as.numeric(data)

#dataOrdered = data[order(data)]
#print(dataOrdered)

counts = rep(0, length(targets))
for(i in 1:length(targets)){
	counts[i] = max(which(data0 > targets[i]))
}
#print(counts)


plotCircle = function(x,y,text){
	for(i in length(x):1){
		points(x[i], y[i], pch=21, cex=3, lw=2, col="black", bg="white", type='p')
		text(x[i], y[i], text[i])
	}
}


barColor0 = rgb(0.0,0.5,1.0)
barColor7 = rgb(0.3,0.65,1.0) #rgb(0.0,0.5,1.0,0.7)
barColor14 = rgb(0.5,0.75,1.0) #rgb(0.0,0.5,1.0,0.5)
barColor21 = rgb(0.8,0.9,1.0) #rgb(0.0,0.5,1.0,0.2)

targetColor1 = rgb(1.0,0.2,0.2,0.3)
targetColor2 = rgb(1.0,0.2,0.2,0.7)
targetColor3 = rgb(1.0,0.2,0.2,1.0)




offset = 200

#fileName = paste(studyId,paste("points","pdf",sep="."),sep="_")
fileName = "points.pdf"
pdf(fileName, pointsize=16, width=12, height=8)
    par(mar=c(4.5,4.5,0.5,0.5))
	#main="Parts Completed by Students"
	plot(c(bounds[1]+20,bounds[2]-20), c(50,length(data0)-150), ylab="Total Number of Students", xlab="Points Awarded", main="", type='n') #, panel.first=grid()
	
	for(i in 1:length(targets)){
		points(c(targets[i],targets[i]), c(counts[i],-500), type='l', lty=1, lw=3, col=rgb(0.0,0.0,0.0,0.2))
		if(counts[i]<goal){
			points(c(targets[i],targets[i]), c(goal,counts[i]), type='l', lw=3, col=targetColor2) #col=rgb(0.0,0.0,0.0,0.5)
		}
		#abline(v=targets[i], lw=1, col=targetColor1, lty=2)
		
		#points(c(-500,targets[i]), c(counts[i],counts[i]), type='l', lw=3, col=rgb(0.0,0.0,0.0,1.0))
	}
	#points(targets, goals-offset, pch=21, cex=3, lw=2, col="black", bg="white", type='p')
	#text(targets, goals-offset, 1:length(targets))
	
	points(c(-100,tail(targets,1)), c(goal,goal), type='l', lw=3, col=rgb(0.0,0.0,0.0,1.0), lty=1)
	#points(c(tail(targets,1),tail(targets,1)), c(goal,-500), type='l', lw=3, col=targetColor3, lty=1)
	
	points(data0, 1:length(data0), type='l', lw=4, col=barColor0)
	points(data7, 1:length(data7), type='l', lw=4, col=barColor7)
	points(data14, 1:length(data14), type='l', lw=4, col=barColor14)
	points(data21, 1:length(data21), type='l', lw=4, col=barColor21)
	
	plotCircle(targets, counts-offset, 1:length(targets))
	#plotCircle(targets, rep(0, length(targets)), 1:length(targets))
	
	#plotCircle(rep(0, length(targets)), counts, 1:length(targets))
	


	legend("topright", c("Present", "1 Week Ago", "2 Weeks Ago", "3 Weeks Ago", "Our Dream", "Assignment"), cex=1.0, pch=c(-1,-1,-1,-1,-1, 21), lwd=c(4,4,4,4,3,2), lty=c(1,1,1,1,1,-1), col=c(barColor0,barColor7,barColor14,barColor21,"black","black"), bg="white");
dev.off()