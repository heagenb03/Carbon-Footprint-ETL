suppressPackageStartupMessages({
  library(DBI)
  library(RMariaDB)
  library(ggplot2)
  library(dplyr)
  library(tidyr)
  library(readr)
  library(dotenv)
})

load_dot_env(file = ".env")
mysql_user <- Sys.getenv("MYSQL_USER")
mysql_password <- Sys.getenv("MYSQL_PASSWORD")
mysql_db <- Sys.getenv("MYSQL_DB")

con <- dbConnect(
  RMariaDB::MariaDB(),
  host = "localhost",
  user = mysql_user,
  password = mysql_password,
  dbname = mysql_db
)

electricity_df <- dbReadTable(con, "electricity")
flight_df <- dbReadTable(con, "flight")
shipping_df <- dbReadTable(con, "shipping")
vehicle_df <- dbReadTable(con, "vehicle")

output_dir <- file.path(getwd(), "figures")

# Electricity DB
if (!is.null(electricity_df)) {
  expected_cols <- c("country", "state", "electricity_value",
                     "electricity_unit", "carbon_emission")
  missing_cols <- setdiff(expected_cols, names(electricity_df))
  if (length(missing_cols) == 0) {
    electricity_summary <- electricity_df %>%
      mutate(location = ifelse(is.na(state) | state == "",
                               country,
                               paste(country, state, sep = ", "))) %>%
      group_by(location) %>%
      summarize(total_emission = sum(as.numeric(carbon_emission),
                                     na.rm = TRUE),
                .groups = "drop") %>%
      arrange(desc(total_emission))

    p <- ggplot(electricity_summary,
                aes(x = reorder(location, total_emission),
                    y = total_emission)) +
      geom_col(fill = "#2E86AB") +
      coord_flip() +
      labs(title = "Electricity Emissions by Location",
           x = "Location",
           y = "Total CO2e") +
      theme_minimal()

    ggsave(filename = file.path(output_dir,
                                "electricity_emissions_by_location.png"),
           plot = p,
           width = 9,
           height = 6,
           dpi = 150)
  }
}

# Flight DB
if (!is.null(flight_df)) {
  expected_cols <- c("passengers", "departure", "destination",
                     "round_trip", "carbon_emission")
  missing_cols <- setdiff(expected_cols, names(flight_df))
  if (length(missing_cols) == 0) {
    flight_df <- flight_df %>%
      mutate(route = paste(departure, destination, sep = " → "))

    p <- ggplot(flight_df,
                aes(x = route,
                    y = as.numeric(carbon_emission),
                    fill = as.factor(passengers))) +
      geom_col(position = "dodge") +
      coord_flip() +
      labs(title = "Flight Emissions by Route",
           x = "Route",
           y = "CO2e",
           fill = "Passengers") +
      theme_minimal()

    ggsave(filename = file.path(output_dir, "flight_emissions_by_route.png"),
           plot = p,
           width = 10,
           height = 6,
           dpi = 150)
  }
}

# Shipping DB
if (!is.null(shipping_df)) {
  expected_cols <- c("weight_value", "weight_unit", "distance_value",
                     "distance_unit", "transport_method", "carbon_emission")
  missing_cols <- setdiff(expected_cols, names(shipping_df))
  if (length(missing_cols) == 0) {
    shipping_summary <- shipping_df %>%
      group_by(transport_method) %>%
      summarize(total_emission = sum(as.numeric(carbon_emission),
                                     na.rm = TRUE),
                .groups = "drop") %>%
      arrange(desc(total_emission))

    p <- ggplot(shipping_summary,
                aes(x = reorder(transport_method, total_emission),
                    y = total_emission)) +
      geom_col(fill = "#8E44AD") +
      coord_flip() +
      labs(title = "Shipping Emissions by Transport Method",
           x = "Transport Method",
           y = "Total CO2e") +
      theme_minimal()

    ggsave(filename = file.path(output_dir,
                                "shipping_emissions_by_transport.png"),
           plot = p,
           width = 9,
           height = 6,
           dpi = 150)
  }
}

# Vehicle DB
if (!is.null(vehicle_df)) {
  expected_cols <- c("distance_value", "distance_unit", "vehicle_make",
                     "vehicle_name", "vehicle_year", "carbon_emission")
  missing_cols <- setdiff(expected_cols, names(vehicle_df))
  if (length(missing_cols) == 0) {
    vehicle_df <- vehicle_df %>%
      mutate(vehicle = paste(vehicle_make, vehicle_name, vehicle_year))
    p <- ggplot(vehicle_df, aes(x = vehicle, y = as.numeric(carbon_emission))) +
      geom_col(fill = "#27AE60") +
      coord_flip() +
      labs(title = "Vehicle Emissions",
           x = "Vehicle",
           y = "CO2e") +
      theme_minimal()

    ggsave(filename = file.path(output_dir, "vehicle_emissions.png"),
           plot = p,
           width = 9,
           height = 6,
           dpi = 150)
  }
}

# Overview
category_totals <- list(
  electricity = if (!is.null(electricity_df)) {
    sum(as.numeric(electricity_df$carbon_emission), na.rm = TRUE)
  } else {
    NA_real_
  },
  flight = if (!is.null(flight_df)) {
    sum(as.numeric(flight_df$carbon_emission), na.rm = TRUE)
  } else {
    NA_real_
  },
  shipping = if (!is.null(shipping_df)) {
    sum(as.numeric(shipping_df$carbon_emission), na.rm = TRUE)
  } else {
    NA_real_
  },
  vehicle = if (!is.null(vehicle_df)) {
    sum(as.numeric(vehicle_df$carbon_emission), na.rm = TRUE)
  } else {
    NA_real_
  }
) %>%
  unlist(use.names = TRUE) %>%
  tibble::enframe(name = "category", value = "total_emission") %>%
  filter(!is.na(total_emission))

if (nrow(category_totals) > 0) {
  p <- ggplot(category_totals,
              aes(x = reorder(category, total_emission),
                  y = total_emission)) +
    geom_col(fill = "#F39C12") +
    coord_flip() +
    labs(title = "Total Emissions by Category",
         x = "Category",
         y = "Total CO2e") +
    theme_minimal()

  ggsave(filename = file.path(output_dir,
                              "total_emissions_by_category.png"),
         plot = p,
         width = 8,
         height = 5,
         dpi = 150)
}

dbDisconnect(con)
