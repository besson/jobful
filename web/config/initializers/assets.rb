# Be sure to restart your server when you modify this file.

# Version of your assets, change this if you want to expire all your assets.
Rails.application.config.assets.version = '1.0'
Rails.application.config.assets.precompile += %w( d3.v3.min.js )
Rails.application.config.assets.precompile += %w( topojson.v1.min.js )
Rails.application.config.assets.precompile += %w( datamaps.all.min.js )
Rails.application.config.assets.precompile += %w( map.js )
Rails.application.config.assets.precompile += %w( chart.js )

Rails.application.config.assets.precompile += %w( bootstrap.min.css )
Rails.application.config.assets.precompile += %w( agency.css )
Rails.application.config.assets.precompile += %w( font-awesome.min.css )

# Precompile additional assets.
# application.js, application.css, and all non-JS/CSS in app/assets folder are already added.
# Rails.application.config.assets.precompile += %w( search.js )
