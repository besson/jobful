class Category < ActiveRecord::Base
  has_many :categorizations
  has_many :bubbles, through: :categorizations
end
