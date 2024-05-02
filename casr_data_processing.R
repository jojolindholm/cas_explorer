library(casr)
library(tidyverse)

load("/Users/johanlindholm/Dropbox/Arbete/Forskning/Projekt/Court of Arbitration for Sport/casr/data/info_arbitrators.rda")

info_arbitrators <- info_arbitrators |> 
  add_history_to_info_arbitrators() |> 
  mutate(delisted = !is.na(listed_last),
         delisted_age = listed_last - born_year,
         years_listed = listed_last - listed_first) |> 
  

write_csv(info_arbitrators, "/Users/johanlindholm/Dropbox/Arbete/Annat/Experiment/streamlit_test/info_arbitrators.csv")

