library("data.table")
library("plotly")
library("tidyr")
library("htmlwidgets")
library("RColorBrewer")

files = list("Simulation-Calibrated-General" ,"Simulation-ForwardMeasure-General", "Simulation-SpotMeasure-General", "Simulation-ForwardMeasure-Martingale", "Simulation-SpotMeasure-Martingale")
file = files[[1]]
data = fread(paste(file,".csv", sep=""))
head(data)

mFig <- plot_ly()

mFig <- mFig %>% layout(
  title = list(text = "LIBOR Forward Rate Curve", font = list(size = 20)),
  xaxis = list(
    title = list(text = "Time Steps", font = list(size = 10)),
    font = list(size = 5),
    tickmode = 'array',
    tickvals = round(data$time[seq(0,length(data$time),126)], 2)
  ),  
  yaxis = list(title = list(text = "Forward Rate", font = list(size = 10))),
  legend = list(title = list(text = 'Lines', font = list(size = 5))),
  hovermode = 'x'
)

colors <- brewer.pal(n = length(setdiff(colnames(data), c("epoch", "Time"))), name = "Set1")

#for (i in iterations) {
df <- data
cols <- setdiff(colnames(df), c("time"))
for (j in seq_along(cols)) {
  col <- cols[j]
  mFig <- mFig %>% add_trace(
    x = df$time, y = df[[col]],
    type = 'scatter',
    mode = 'lines',
    name = col,
    line = list(width = 1, color = colors[j]),
    hoverinfo = 'text',
    text = paste("t= ", round(df$time, 2), ": ", round(df[[col]], 4)),
    visible = TRUE
  )
}

saveWidget(mFig, paste(file,".html", sep=""), selfcontained = TRUE)
mFig

