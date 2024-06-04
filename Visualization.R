library("data.table")
library("plotly")
library("tidyr")
library("htmlwidgets")
library("RColorBrewer")

files = list("Simulation-ForwardMeasure-General", "Simulation-SpotMeasure-General", "Simulation-ForwardMeasure-Martingale", "Simulation-SpotMeasure-Martingale")
data = fread(paste(files[[2]],".csv", sep=""))
head(data)

noi = 5
epoch = unique(data$epoch)
iterations = sample(epoch, noi, replace=FALSE)

steps <- lapply(iterations, function(i) {
  list(
    args = list("visible", rep(FALSE, length(iterations) * length(setdiff(colnames(data), c("epoch","Time"))))),
    label = paste("Iteration", i),
    method = "restyle"
  )
})

for (i in seq_along(steps)) {
  steps[[i]]$args[[2]][((i - 1) * length(setdiff(colnames(data), c("epoch", "Time"))) + 1):(i * length(setdiff(colnames(data), c("epoch","Time"))))] <- TRUE
}

mFig <- plot_ly()

mFig <- mFig %>% layout(
  title = list(text = "(Sexy-) LIBOR Curves", font = list(size = 20)),
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

saveWidget(mFig, paste(files[[2]],".html", sep=""), selfcontained = TRUE)
mFig

