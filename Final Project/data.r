library(tidyverse)

options(stringsAsFactors =  FALSE)

players <- data.frame(name = c("許亦佐", "許亦佑", "惟小"), student_id = c(1, 21, 3), 
                      sex = c(1, 1, 0), grade = c(50, 100, 75), tel = c("NaN", "NaN", "要問許亦佑才知道"),
                      photo = c("NaN", "NaN", "NaN"), card_front = c("NaN", "NaN", "NaN"),
                      card_back = c("NaN", "NaN", "NaN"), liscence = c("NaN", "NaN", "NaN"),
                      at_school_proof = c("NaN", "NaN", "NaN"))

playing_sports <- data.frame(student_id = c(1,2,3),
                             sport = c("69", "69", "69"),
                             points_left = c(1,3,5),
                             points_received = c(2,4,6))

team <- data.frame(sport = c("羽球", "籃球", "甲蟲王者", "羅馬競技生死鬥"),
                   captain_id = c(21, 21, 21, 21))

trainings <- data.frame(time = c("21:00", "05:00", "13:00"),
                        court = c("管圖", "管五", "你家"))

