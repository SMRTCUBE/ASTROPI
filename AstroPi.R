#Analysis and Mapping for AstroPi Data
#Version 1.0
#18 Jun 2022



library(PerformanceAnalytics)
my_data <- read.csv(file.choose())
head(my_data, 6)
res <- cor(my_data)
res1 <- round(res, 2)
write.csv(res1, "~\\Correlation.csv")
chart.Correlation(my_data, histogram = TRUE, method = "pearson")

#Set up the surface plots for Magnetometer(x,y,z) vs Lat/Long
ibrary(ggmap)
library(sf)
library(ggplot2)

library(lubridate)
library(dplyr)
library(data.table)
library(ggrepel)
library(tidyverse)

#Register Google API Key for ggmap library

register_google(key="") # API Key Removed for public submission

mag_data <- read.csv(file.choose(), stringsAsFactors = FALSE)
head(mag_data)
dim(mag_data)
attach(mag_data)
col1 = "#011f4b"
col2 = "#6497b1"
col3 = "#b3cde0"
col4 = "#CC0000"

i2 <- data.table(mag_data)

p <- ggmap(get_googlemap(center = c(lon = 0, lat = 0),
                         zoom = 1, scale = 1,
                         maptype ='terrain',
                         color = 'color'))
p + geom_point(aes(x = Longtitude, y = Lattitude), data = i2, size = 0.5) + 
  theme(legend.position="bottom")
