class RemoveMetricIdFromBubble < ActiveRecord::Migration
  def change
    remove_column :bubbles, :metric_id
  end
end
