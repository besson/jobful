class CreateCategorizations < ActiveRecord::Migration
  def change
    create_table :categorizations do |t|
      t.integer :bubble_id
      t.integer :category_id
    end
    add_index :categorizations, [:bubble_id, :category_id]
  end
end
