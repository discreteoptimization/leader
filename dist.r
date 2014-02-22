studyId = "test"
dataFile = "1_1_quality.data"
sense = 1
name = "Testing"
threshold1 = 8
threshold2 = 6

args = commandArgs(TRUE)
print(args)
if(length(args) == 6){
   studyId = args[[1]]
   dataFile = args[[2]]
   sense = as.numeric(args[[3]])
   name = args[[4]]
   threshold1 = as.numeric(args[[5]])
   threshold2 = as.numeric(args[[6]])
}

name = gsub("_"," ",name)

data = read.csv(dataFile,header=FALSE,sep=",",stringsAsFactors=TRUE)
data = as.numeric(data)

z = quantile(data,c(0.01,0.05,0.1,0.2,0.5,0.8,0.9))
#print(z)

#print(data)
#print(length(data))

if(sense == 0){
        #print('MIN')
        #data = data[data >= as.numeric(z[4])]
        
        best_val = min(data)
        delta = threshold1 - best_val
        cutoff = threshold1 + delta
        data = data[data <= cutoff]
} else {
        #print('MAX')
        #data = data[data <= as.numeric(z[6])]
        
        best_val = max(data)
        delta = threshold1 - best_val
        cutoff = threshold1 + delta
        data = data[data >= cutoff]
}

#print(data)
#print(length(data))

#barColor = rgb(0.0,0.5,1.0,1.0)
#barColor = rgb(0.0,0.4,0.6,1.0) #tbl dark 1
barColor = rgb(0.0,0.33,0.5,1.0) #tbl dark 2
#barColor = rgb(0.88,0.93,0.96,1.0) #tbl light
threshold1Color = rgb(0.15,0.5,1.0,1.0)
threshold2Color = rgb(1.0,0.5,0.0,1.0)

targetColor = rgb(1.0,0.2,0.2,0.8)

lineColor = rgb(0.0,0.0,0.0,0.3)
pointColor = rgb(0.0,0.0,0.0,0.3)
pointStyle = c(1,19)

fileName = paste(studyId,paste("dist","pdf",sep="."),sep="_")
pdf(fileName, pointsize=18, width=9, height=9)
	par(mar=c(4.5,4.5,0.5,0.5))
	nBreaks = max(1,min(40, max(data)-min(data)))
	
	if(nBreaks == 1){
		lim = c(min(data)-0.5,max(data)+0.5)
		hist(data, breaks=nBreaks, col=barColor, border='black', ylab="Solution Count", xlab="Objective Value", main="", xlim=lim) #, main=name
	} else {
		hist(data, breaks=nBreaks, col=barColor, border='black', ylab="Solution Count", xlab="Objective Value", main="")
	}
	abline(v=median(data), lw=6, col=targetColor)
	
	#if(threshold1 > 0){
	#	abline(v=threshold1, lw=6, col=threshold1Color)
	#}
	#abline(v=threshold2, lw=6, col=threshold2Color)
dev.off()