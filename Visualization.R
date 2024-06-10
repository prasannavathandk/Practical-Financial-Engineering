library("data.table")
library("plotly")
library("tidyr")
library("htmlwidgets")
library("RColorBrewer")

files = list("Simulation-ForwardMeasure-General", "Simulation-SpotMeasure-General", "Simulation-ForwardMeasure-Martingale", "Simulation-SpotMeasure-Martingale")
file = files[[1]]
data = fread(paste(file,".csv", sep=""))
head(data)

average <- data[, lapply(.SD, mean), by = Time, .SDcols = setdiff(colnames(data), c("Time"))]
average$epoch = 0
setindex(average, epoch)
print(average)
data <- rbind(data, average)


noi = 4
epoch = unique(data$epoch)
iterations = sample(epoch[epoch != 0], noi, replace=FALSE)
iterations= c(iterations, c(0))

steps <- lapply(iterations, function(i) {
  list(
    args = list("visible", rep(FALSE, length(iterations) * length(setdiff(colnames(data), c("epoch","Time"))))),
    label = ifelse(i != 0, paste("Iteration", i), "Expectation"),
    method = "restyle"
  )
})

for (i in seq_along(steps)) {
  steps[[i]]$args[[2]][((i - 1) * length(setdiff(colnames(data), c("epoch", "Time"))) + 1):(i * length(setdiff(colnames(data), c("epoch","Time"))))] <- TRUE
}

mFig <- plot_ly()

mFig <- mFig %>% layout(
  title = list(text = paste("LIBOR Forward Rate Curve",file) , font = list(size = 20)),
  sliders = list(
    list(
      active = 0,
      currentvalue = list(prefix = "Iteration: "),
      pad = list(t = 30),
      font = list(size = 5),
      steps = steps
    )
  ),
    xaxis = list(
      title = list(text = "Time Steps", font = list(size = 10)),
      font = list(size = 5),
      tickmode = 'array',
      tickvals = round(data[epoch == 1,,]$Time[seq(0,length(data[epoch == 1,,]$Time),126)], 2)
    ),  
    yaxis = list(title = list(text = "Forward Rate", font = list(size = 10))),
    legend = list(title = list(text = 'Lines', font = list(size = 5))),
    hovermode = 'x'
  )

colors <- brewer.pal(n = length(setdiff(colnames(data), c("epoch", "Time"))), name = "Set1")

for (i in iterations) {
  df <- data[epoch == i]
  cols <- setdiff(colnames(df), c("epoch", "Time"))
  for (j in seq_along(cols)) {
    col <- cols[j]
    mFig <- mFig %>% add_trace(
      x = df$Time, y = df[[col]],
      type = 'scatter',
      mode = 'lines',
      name = col,
      line = list(width = 1, color = colors[j]),
      hoverinfo = 'text',
      text = paste("t= ", round(df$Time, 2), ": ", round(df[[col]], 4)),
      visible = TRUE
    )
  }
}

saveWidget(mFig, paste(file,".html", sep=""), selfcontained = TRUE)
mFig

