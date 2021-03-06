library(dplyr)
library(ggplot2)
library(chron)
load("C:/Users/super/Desktop/CHIDS/MedStar/UMD CHIDS Data Final Version.RData")

# distinct variables for a row
distinct__ <- function(r)
{
  if (is.null(r) | length(r) == 0)
  {
    return(NULL)
  }
  
  if (!is(r, "character"))
  {
    for (i in 1:length(r))
    {
      r[0] <- toString(r[0])
    }
  }
  
  buffer <- list()
  cbuffer <- NULL
  for (i in 1:length(r))
  {
    if (is.null(buffer[[r[i]]]))
    {
      buffer[[r[i]]] <- r[i]
    }
  }
  
  for (i in buffer)
  {
    cbuffer <- c(cbuffer, i)
  }
  return(cbuffer)
}


# date of birth distribution
PDOB <- doclist %>% select(DATEOFBIRTH, PID)
PDOB <- PDOB[!duplicated(PDOB),]
# approximate extimates of age
PDOB$DATEOFBIRTH <- substr(PDOB$DATEOFBIRTH,1,4)
PDOB$age <- 2019 - as.numeric(PDOB$DATEOFBIRTH)

mean(PDOB$age)  # 67
ggplot(PDOB, aes(x=age)) +
  geom_bar(stat='count') +
  scale_y_continuous("number of age", expand=c(0,0))

# more dist
pstat <- joineddata %>% select(PID, SEX, RACE)
pstat <- pstat[!duplicated(pstat),]
length(distinct__(pstat$PID)) # 1000

# sex dist
ggplot(pstat, aes(x=RACE, fill=factor(SEX))) + 
  geom_bar(position='fill', stat='count', aes(fill = SEX, y = ..count../sum(..count..))) +
  scale_y_continuous("Proportion of sexes", expand=c(0,0)) + 
  scale_fill_manual("Sex", values=c("pink","blue"), labels=c("Female","Male")) +
  theme_minimal()


# BEHAVIOORAL CATEGORY
  
# physical activity
# exploring...
pa <- obsdata %>% select(HDID, NAME, DESCRIPTION)
pa <- pa[!duplicated(pa),]
pa %>% filter(grepl("physical", DESCRIPTION, fixed=TRUE)) %>% filter(!grepl("exam", DESCRIPTION, fixed=TRUE))
# physical exercise = 128
sum(obsdata$HDID == 128)

# smoking status/tobacco use
pa %>% filter(grepl("smok", DESCRIPTION, fixed=TRUE))
pa %>% filter(grepl("tobacco", DESCRIPTION, fixed=TRUE))
# total pack/day = 2622, has 1285 records
sum(obsdata$OBSVALUE[obsdata$HDID == 2622] != 0 & obsdata$OBSVALUE[obsdata$HDID == 2622] != 'no' & obsdata$OBSVALUE[obsdata$HDID == 2622] != 'none')
# total pack/day = 2621, has 795 records, overlaps with 2622
sum(obsdata$OBSVALUE[obsdata$HDID == 2621] != 0 & obsdata$OBSVALUE[obsdata$HDID == 2621] != 'no' & obsdata$OBSVALUE[obsdata$HDID == 2621] != 'none')
# years of smoking (dirty)
# date end
obsdata[obsdata$HDID == 300016,][!duplicated(obsdata[obsdata$HDID == 300016,]$OBSVALUE),]$OBSVALUE
# date start
obsdata[obsdata$HDID == 300017,][!duplicated(obsdata[obsdata$HDID == 300017,]$OBSVALUE),]$OBSVALUE
# cigars week = 43531, has only 49 records
sum(obsdata$OBSVALUE[obsdata$HDID == 43531] != 0 & obsdata$OBSVALUE[obsdata$HDID == 43531] != 'no' & obsdata$OBSVALUE[obsdata$HDID == 43531] != 'none')
# cigars day = 16028, has only 2 records
sum(obsdata$OBSVALUE[obsdata$HDID == 16028] != 0 & obsdata$OBSVALUE[obsdata$HDID == 16028] != 'no' & obsdata$OBSVALUE[obsdata$HDID == 16028] != 'none')
# number of years as a smoker = 17276, has only 10 records
sum(obsdata$OBSVALUE[obsdata$HDID == 17276] != 0 & obsdata$OBSVALUE[obsdata$HDID == 17276] != 'no' & obsdata$OBSVALUE[obsdata$HDID == 17276] != 'none')
# 300015 given is also dirty and thus needs intergrading with aboves
obsdata$OBSVALUE[obsdata$HDID == 300015][!duplicated(obsdata$OBSVALUE[obsdata$HDID == 300015])]

# 3029 tobacco is of no use since the records are all negative.
obsdata[obsdata$HDID == 3029,][obsdata[obsdata$HDID == 3029,]$OBSVALUE != 'none' & obsdata[obsdata$HDID == 3029,]$OBSVALUE != 0,]
# tobacco year = 22099, has only 2 records
sum(obsdata$OBSVALUE[obsdata$HDID == 22099] != 0 & obsdata$OBSVALUE[obsdata$HDID == 22099] != 'no' & obsdata$OBSVALUE[obsdata$HDID == 22099] != 'none')
# take a look at comments, it also contains information that could contributes years of smoking or years of stop smoking
obsdata[obsdata$HDID == 300019,][!duplicated(obsdata[obsdata$HDID == 300019,]$OBSVALUE),]$OBSVALUE

# alcohol use
pa %>% filter(grepl("alcohol", DESCRIPTION, fixed=TRUE))
obsdata[obsdata$HDID == 2313,][!duplicated(obsdata[obsdata$HDID == 2313,]$OBSVALUE),]$OBSVALUE
sum(obsdata[obsdata$HDID == 2313,]$OBSVALUE != 'none')   # 7792

#body weight control
pa %>% filter(grepl("diet", DESCRIPTION, fixed=TRUE))
# compliant with recommended diet has only 33 records
obsdata[obsdata$HDID == 30801,]
# Diabetes Care Management: dietary compliance has 127 records
obsdata[obsdata$HDID == 229072,]

# medication adherence
pa %>% filter(grepl("compli", DESCRIPTION, fixed=TRUE))
obsdata[obsdata$HDID == 157943,][!duplicated(obsdata[obsdata$HDID == 157943,]$OBSVALUE),]$OBSVALUE
sum(obsdata$HDID == 157943) #104
# compliance with medical treatment
sum(obsdata$HDID == 2540)   #18316

# diet habit
# diabetes diet management
sum(obsdata$HDID == 120295)   #98
obsdata[obsdata$HDID == 120295,][!duplicated(obsdata[obsdata$HDID == 120295,]$OBSVALUE),]$OBSVALUE
obsdata[obsdata$HDID == 120295,]
# diet plan (simple dummies will do)
sum(obsdata$HDID == 2832)   #41
obsdata[obsdata$HDID == 2832,]

# sleep NOT FOUND
pa %>% filter(grepl("sleep", DESCRIPTION, fixed=TRUE))
obsdata[obsdata$HDID == 32278,]   # what does referred mean? 32278 SLEEPAPNCOMM sleep apnea, hx of, comments <NA> MLI-32278    <NA> 2014-10-27 09:27:56.0       T referred

# TODO: appointments
apt_cnt <- doclist %>% count(PID)
apt_cnt


# PSYCHOLOGICAL CATEGORY

# depression



# A1C clean
# TODO: may not be the best way to classify patients.
is_prediebete <- function(patient_A1C_history, tolerance=1)
{
  # tolearace: a1c flcturation through diabetes status
  
  # TRUNCATED   2/11/2020
  # if (sum(patient_A1C_history$A1C < 6.5) > 0 & sum(patient_A1C_history$A1C >= 6.5) > 0)
  # {
  #   return(TRUE)
  # }
  # return(FALSE)
  
  
  # flag_p2d: 0: normal period, 1: pre-diebetes period, 2: diebetes period
  flag_p2d <- 0
  threshold <- 0
  patient_A1C_history <- patient_A1C_history[order(patient_A1C_history$OBSDATEf),]
  for (i in patient_A1C_history$A1C)
  {
    if (flag_p2d == 0 & i < 5.7)
    {
      next
    }
    else if (flag_p2d <= 1 & i >= 5.7 & i < 6.5)
    {
      flag_p2d <- 1
    }
    else if (flag_p2d >= 1 & flag_p2d <= 2 & i >= 6.5)
    {
      flag_p2d <- 2
    }
    else if (threshold >= tolerance)
    {
      return(F)
    }
    else
    {
      threshold <- threshold + 1
    }
  }
  
  if (i >= 6.5)
  {
    return(T)
  }
  return(F)
}

a1c_valid_filter <- function()
{
  # filter out useless a1cs ("Pending", "*", "<3.5%")
  a1c_data <- a1c[a1c$A1C != 'Pending' & a1c$A1C != '*' & a1c$A1C != '<3.5 %',]
  for (i in 1: dim(a1c_data)[1])
  {
    # extract a1c numeric in a1c string
    a1c_str <- strsplit(a1c_data$A1C[i]," % OF TOTAL HGB")[[1]]
    a1c_data$A1C[i] <- strsplit(a1c_str," %")[[1]]
    # for debug use
    if (is.na(as.numeric(a1c_str)))
    {
      print(i)
    }
  }
  # transform into numeric
  a1c_data$A1C <- as.numeric(a1c_data$A1C)
  return(a1c_data)
}

a1c_prediebete2diebete_filter <- function(a1c_valid, tolerance=1)
{
  cBuffer <- NULL
  for (pid in distinct__(a1c_valid$PID))
  {
    # fetch a1c history for a single patient
    patient_A1C_history <- a1c_valid[a1c_valid$PID == pid,]
    if (is_prediebete(patient_A1C_history, tolerance = tolerance))
    {
      cBuffer <- c(cBuffer, pid)
    }
  }
  # return array of matched PID
  return(cBuffer)
}

a1c_valid <- a1c_valid_filter()

#Reclassifying OBSDATE var from character to date and time using chron function.
dtparts <- t(as.data.frame(strsplit(a1c_valid$OBSDATE,' ')))
row.names(dtparts) = NULL
formatteddates <- chron(dates=dtparts[,1],times=dtparts[,2], format=c('y-m-d','h:m:s'))
#adding formatted OBSDATE to a1c df.
a1c_valid$OBSDATEf <- formatteddates
a1c_valid$OBSYEAR <-years(a1c_valid$OBSDATEf)

PID_filtered <- a1c_prediebete2diebete_filter(a1c_valid, tolerance = 1) # takes 20 secs
length(PID_filtered)  # 96


# Margret's needs
library("plotly")

ma1c <- a1c_valid[a1c_valid$OBSYEAR >= 2012 & a1c_valid$OBSYEAR <= 2016,]
a1c_grouped_year <- ma1c %>% group_by(PID, OBSYEAR) %>% summarise(mean_a1c = mean(A1C, na.rm=T))
a1c_grouped_year <- as.data.frame(a1c_grouped_year)

# try to make a frame with year in the columns in order to make a clear graph afterwards
PID <- distinct__(ma1c$PID)
a1c_12_16 <- data.frame(PID)

# Completed two targets in the underlying for loop:
# 1, tagged patients who were transformed from pre-diabetes to diabetes
# 2, transformed aggregated year data into 2-dimension data
for (i in 1: length(a1c_12_16$PID))
{
  # add tag if is included in our pre-diabetes-to-diabetes patients
  pid <- a1c_12_16$PID[i]
  for (p_v in PID_filtered)
  {
    if (p_v == pid)
    {
      a1c_12_16[i, 'patient_type'] <- 'pre-diabetes-to-diabetes'
    }
  }
  # extract average a1c each year observed for each patient
  single_patient <- a1c_grouped_year[a1c_grouped_year$PID == pid,]
  for (j in 1: length(single_patient$OBSYEAR))
  {
    # stringnify observe year to slice and assign to a1c_12_16
    observe_year <- single_patient$OBSYEAR[j]
    a1c_12_16[i, toString(observe_year)] <- single_patient$mean_a1c[j]
  }
}
a1c_12_16$patient_type[is.na(a1c_12_16$patient_type)] <- 'Normal or pre-diabetes'
a1c_12_16_p2d <- a1c_12_16[a1c_12_16$patient_type == 'pre-diabetes-to-diabetes',]
a1c_12_16_np <- a1c_12_16[!a1c_12_16$patient_type == 'pre-diabetes-to-diabetes',]

# Parallel Coordinate Graph for all A1C
p_ <- GGally::print_if_interactive
p <- ggparcoord(data=a1c_12_16, columns=c(3:7), groupColumn=2, missing='exclude',scale = "globalminmax", title = "All patients' A1C in 2012~2016", alphaLines = 0.4)
p_(p + xlab("Year") + ylab("A1C"))

p <- ggparcoord(data=a1c_12_16_p2d, columns=c(3:7), groupColumn=2, missing='mean',scale = "globalminmax", title = "Pre-diabetes-to-diabetes patients' A1C records in 2012~2016", alphaLines = 0.4)
p_(p + xlab("Year") + ylab("A1C"))

p <- ggparcoord(data=a1c_12_16_np, columns=c(3:7), groupColumn=2, missing='mean',scale = "globalminmax", title = "Excluded A1C records in 2012~2016", alphaLines = 0.4)
p_(p + theme(legend.position = 'none') + xlab("Year") + ylab("A1C"))

# we don't have stdeviation from the statistic table
sd(a1c_12_16_p2d[!is.na(a1c_12_16_p2d[,3]),3])
# 0.8031698
sd(a1c_12_16_p2d[!is.na(a1c_12_16_p2d[,4]),4])
# 0.8459552
sd(a1c_12_16_p2d[!is.na(a1c_12_16_p2d[,5]),5])
# 0.7453513
sd(a1c_12_16_p2d[!is.na(a1c_12_16_p2d[,6]),6])
# 0.8735061
sd(a1c_12_16_p2d[!is.na(a1c_12_16_p2d[,7]),7])
# 0.889422

sd(a1c_12_16_np[!is.na(a1c_12_16_np[,3]),3])
# 0.2379879
sd(a1c_12_16_np[!is.na(a1c_12_16_np[,4]),4])
# 0.2382006
sd(a1c_12_16_np[!is.na(a1c_12_16_np[,5]),5])
# 0.2412425
sd(a1c_12_16_np[!is.na(a1c_12_16_np[,6]),6])
# 0.2433891
sd(a1c_12_16_np[!is.na(a1c_12_16_np[,7]),7])
# 0.2503714


# We need to merge categories to one single df
# Invariant categories:
included_HDID <- c(3030, 2303, 
                   8087, 7,
                   40, 2788,
                   128, 2622,
                   2621, 300017, 
                   300016, 300015,
                   500017,
                   2313, 2540,
                   229072,
                   126176,
                   14, 28,
                   17300068,
                   44,
                   2738, 
                   2664, 8833,
                   77728,
                   61, 3095, 
                   156251,4705,
                   3889
)
PID_SDID_CATEGORIES_col_name <- c("level of education", "diabetes mellitus, family hx",
                                  "diabetes mellitus, type", "blood glucose, fasting",
                                  "alanine aminotransferase (SGPT), serum", "body mass index",
                                  "physical exercise, frequency, days per week", "smoking history, total pack/day",
                                  "smoking history, total pack/year", "smoking, date started",
                                  "smoking, year quit", "smoking status",
                                  "smoking, advice to quit",
                                  "alcohol use, average drinks per day", "compliance with medical treatment",
                                  "Diabetes Care Management: dietary compliance",
                                  "Patient Health Questionnaire, feeling down, depressed or hopeless",
                                  "cholesterol, serum", "hemoglobin A1C, blood, as % of total hemoglobin",
                                  "hypertension, hx of",
                                  "triglyceride, serum, fasting",
                                  "caffeine use, average drinks per day", 
                                  "exercise time", "exercise type",
                                  "diet comments",
                                  "weight E&M", "weight in kilograms E&M",
                                  "Weight Management Counseling Provided","family history reviewed E&M",
                                  "blood glucose, finger stick"
)

SDID_HDID_merge <- function(HDID_list, col_names)
{
  category <- joineddata %>% select(PID, SEX, RACE, ETHNICITY, DATEOFBIRTH) %>% distinct()
  PID_SDID_CATEGORIES <- doclist %>% select(PID, SDID) %>% distinct()
  for (hdid in HDID_list)
  {
    HD <- obsdata[obsdata$HDID == hdid, c("SDID", "OBSVALUE")]
    PID_SDID_CATEGORIES <- left_join(PID_SDID_CATEGORIES,
                                 HD,
                                 by='SDID'
    )
  }
  
  # drop na rows
  PID_SDID_CATEGORIES <- PID_SDID_CATEGORIES[rowSums(is.na(PID_SDID_CATEGORIES[3: length(PID_SDID_CATEGORIES)])) != length(PID_SDID_CATEGORIES)-2,]
  # assign col names
  names(PID_SDID_CATEGORIES) <- c("PID", "SDID", col_names)
  # merge joineddata and obsdata with PID
  category <- right_join(category, PID_SDID_CATEGORIES, by='PID')
  return(category)
}

filtered_category <- SDID_HDID_merge(included_HDID, PID_SDID_CATEGORIES_col_name)
info <- obsdata %>% filter(HDID %in% included_HDID) %>% distinct(HDID, DESCRIPTION) %>% order_by(DESCRIPTION)

# make summary for each row
HDID_summary <- function()
{
  all_summary <- data.frame()
  for (hdid in included_HDID)
  {
    summary_tbl <- obsdata %>% filter(HDID==hdid) %>% group_by(HDID, DESCRIPTION, OBSVALUE) %>% summarise(count=n())
    all_summary <- bind_rows(all_summary, summary_tbl)
  }
  return(all_summary)
}

HDID_smy <- HDID_summary()
write.csv(HDID_smy, "C:/Users/super/Desktop/CHIDS/MedStar/HDID_summary.csv", row.names = F)


# TODO: Linear regression discovering
a1c_valid %>% group_by(PID) %>% summarise(minDate=min(OBSDATEf), maxDate=max(OBSDATEf))
joineddata[joineddata$SDID==1550679338564740,]

c <- obsdata %>% group_by(HDID, DESCRIPTION) %>% summarise(count=n()) %>% arrange(desc(count))
c <- unique(obsdata[,c("HDID", "DESCRIPTION")])
write.csv(c, "C:/Users/super/Desktop/CHIDS/MedStar/HDID_DESCRIPTION.csv", row.names = F)
length(obsdata$SDID)

# extract rtf data from doctor's notes in joineddata
for (i in 1:nrow(joineddata))
{
  write(joineddata$NOTE_TEXT[1], paste("E:/desktop_panel/CHIDS/MedStar/rtf/",joineddata$SDID[i],".rtf", sep=''))
}

SDID_HDID_merge_final <- function(HDID_list, col_names)
{
  PID_SDID_CATEGORIES <- finalcombineddoc %>% select(PID, 
                                                     SDID, 
                                                     SEX, 
                                                     RACE, 
                                                     ETHNICITY, 
                                                     DATEOFBIRTH) %>% distinct()
  for (hdid in HDID_list)
  {
    HD <- obsdata[obsdata$HDID == hdid, c("SDID", "OBSVALUE")]
    PID_SDID_CATEGORIES <- left_join(PID_SDID_CATEGORIES,
                                     HD,
                                     by='SDID'
    )
  }
  
  # drop na rows
  PID_SDID_CATEGORIES <- PID_SDID_CATEGORIES[rowSums(is.na(PID_SDID_CATEGORIES[3: length(PID_SDID_CATEGORIES)])) != length(PID_SDID_CATEGORIES)-2,]
  # assign col names
  names(PID_SDID_CATEGORIES) <- c("PID", "SDID", "SEX", "RACE", "ETHNICITY", "DATEOFBIRTH",
                                  col_names)
  return(PID_SDID_CATEGORIES)
}

# get columns of dummies according to selected a1c variables
library("readxl")
dmy_lst <- read_excel("C:/Users/super/Desktop/CHIDS/MedStar/cleaned_HDID_level_summary.xlsx", 
                      sheet = "Sheet1",
                      trim_ws = F)
# dmy_lst <- as.data.frame(dmy_lst)

for (desc in names(filtered_category)[7:length(filtered_category)])
{
  for (i in 1:nrow(filtered_category))
  {
    new_dmy <- dmy_lst[dmy_lst$DESCRIPTION==desc & dmy_lst$OBSVALUE==filtered_category[i, desc], "NEW"]
    if (!is.na(new_dmy[["NEW"]][1]))
    {
      filtered_category[i, paste("dummy", desc, sep='_')] <- new_dmy[["NEW"]][1]
    }
  }
}

write.csv(filtered_category, "E:/desktop_panel/CHIDS/MedStar/final_filtered_HDID_with_dummies.csv", row.names = F, na = "")


# turn selected hdid information into long format data
library(tidyr)
selected_categories <- read_excel("C:/Users/super/Desktop/CHIDS/MedStar/Copy of selected_CATEGORIES(1433).xlsx", 
                                  trim_ws = F)

filtered_category <- SDID_HDID_merge_final(selected_categories$HDID, selected_categories$DESCRIPTION)
HDID_level <- filtered_category %>% select(c(7:length(filtered_category)))
long_HDID_level <- gather(HDID_level, "LEVEL", "NEW", 1:ncol(HDID_level)) %>% group_by(LEVEL, NEW) %>% count()
write.csv(long_HDID_level, "C:/Users/super/Desktop/CHIDS/MedStar/final_HDID_level_summary.csv", row.names = F)

for (i in 1:nrow(finalcombineddoc))
{
  filePath <- paste("[PATH_TO_TARGET_DIR]", finalcombineddoc$SDID[i], ".rtf", 
                    sep='')
  write(finalcombineddoc$NOTE_TEXT[1], filePath)
}

write.csv(finalcombineddoc, "./data/finalcombineddoc.csv", row.names=F)