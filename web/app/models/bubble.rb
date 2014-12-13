class Bubble < ActiveRecord::Base
  belongs_to :metric
  belongs_to :location
  has_many :categorizations
  has_many :categories, through: :categorizations

  def as_json(options={})
    { name: name,
      radius: value <= 50 ? value : 50,
      fillKey: name.split.map(&:chr).join,
      state: location.state,
      latitude: location.latitude,
      longitude: location.longitude
    }
  end
end
