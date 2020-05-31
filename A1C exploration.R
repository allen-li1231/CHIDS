#Exploring a1c dataframe.

#Problem of some values of A1C including characters/text like pending and '% of HGB'.
#use package stringr to extract digits including decimal point.

install.packages(stringr)
library(stringr)
a1cw$A1Cn <- str_extract(a1cw$A1C,"\\d+\\.*\\d*")
a1cw$A1Cn <- as.numeric(a1cw$A1Cn)
summary(a1cw$A1Cn)

#Most A1c observations reported to first decimal plce but a couple reported to hundredths.
#Rounding to first decimal place for consistency.
a1cw$A1Cn <- round(a1cw$A1Cn, digits=1)



#Reclassifying OBSDATE var from character to date and time using chron function.
summary(a1cw$OBSDATE)
dtparts <- t(as.data.frame(strsplit(a1cw$OBSDATE,' ')))
row.names(dtparts) = NULL
formatteddates <- chron(dates=dtparts[,1],times=dtparts[,2], format=c('y-m-d','h:m:s'))
#adding formatted OBSDATE to a1cw df.
a1cw$OBSDATEf <- formatteddates

#Classifying A1Cs in ranges.
a1cw$A1Ccat[5.7<=a1cw$A1Cn & a1cw$A1Cn<=6.4] <- "Prediabetic"
a1cw$A1Ccat[3.51<=a1cw$A1Cn & a1cw$A1Cn<=5.6] <- "Normal"
a1cw$A1Ccat[a1cw$A1Cn >= 6.5] <- "Diabetic"

a1cw$A1Ccat <- as.factor(a1cw$A1Ccat) 
levels(a1cw$A1Ccat)
table(a1cw$A1Ccat)

sum(!is.na(a1cw$A1Ccat))


#Who do we want in our study? Maybe only those who were *first* prediabetic within a 5-year period from 2012-2016?
a1cw$DateCat[a1cw$OBSDATEf < "12-01-01"] <- "Pre-2012"
a1cw$DateCat[a1cw$OBSDATEf >"16-12-31"] <- "Post-2016"
a1cw$DateCat["12-01-01" <= a1cw$OBSDATEf & a1cw$OBSDATEf <= "16-12-31"] <- "2012-2016"
a1cw$DateCat <- as.factor(a1cw$DateCat)
table(a1cw$DateCat)

table(a1cw$DateCat, a1cw$A1Ccat)

#Count number of patients with early A1C obs.
EarlyPeriod <- subset(a1cw, a1cw$DateCat == "Pre-2012")
n_distinct(EarlyPeriod)

#Count number of patients with diabetic or prediabetic observations in Pre-2012 period. 
EarlyElevation <- subset(a1cw, a1cw$DateCat == "Pre-2012" & a1cw$A1Cn > 5.6)
n_distinct(EarlyElevation$PID)

#Quick count of number of observations in target date range for each patient.
targetperiod <- subset(a1cw, a1cw$DateCat == "2012-2016" & !is.na(a1cw$A1Cn))
sum(is.na(targetperiod$A1Cn))

targetA1CPatientlvl <- targetperiod %>%   group_by(PID)   %>%   tally() 
View(targetA1CPatientlvl)
hist(targetA1CPatientlvl$n, main="Number of A1C Measures between 2012-2016", 
     xlab="Number of A1C measures", breaks = 15)
