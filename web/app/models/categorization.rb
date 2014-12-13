class Categorization < ActiveRecord::Base
  belongs_to :bubble
  belongs_to :category
end
