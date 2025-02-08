if (!require(remotes)) install.packages("remotes")
remotes::install_github("prioritizr/aoh")
remotes::install_github("prioritizr/prepr")

# load packages
library(aoh)
library(terra)
library(rappdirs)
library(ggplot2)

IUCN_REDLIST_KEY = "cqZjuvbDn9RVhnZgQPFMccjfkC8oxh3Yp4wR"
is_iucn_rl_api_available()
