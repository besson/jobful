class AddMetricIdToBubbles < ActiveRecord::Migration
  def change
  	add_column :bubbles, :metric_id, :integer
  end
end
