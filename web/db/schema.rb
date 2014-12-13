# encoding: UTF-8
# This file is auto-generated from the current state of the database. Instead
# of editing this file, please use the migrations feature of Active Record to
# incrementally modify your database, and then regenerate this schema definition.
#
# Note that this schema.rb definition is the authoritative source for your
# database schema. If you need to create the application database on another
# system, you should be using db:schema:load, not running all the migrations
# from scratch. The latter is a flawed and unsustainable approach (the more migrations
# you'll amass, the slower it'll run and the greater likelihood for issues).
#
# It's strongly recommended that you check this file into your version control system.

ActiveRecord::Schema.define(version: 20141130155359) do

  create_table "bubbles", force: true do |t|
    t.string  "name"
    t.float   "value"
    t.integer "metric_id"
    t.integer "location_id"
  end

  add_index "bubbles", ["location_id"], name: "index_bubbles_on_location_id"

  create_table "categories", force: true do |t|
    t.string   "name"
    t.datetime "created_at"
    t.datetime "updated_at"
  end

  create_table "categorizations", force: true do |t|
    t.integer "bubble_id"
    t.integer "category_id"
  end

  add_index "categorizations", ["bubble_id", "category_id"], name: "index_categorizations_on_bubble_id_and_category_id"

  create_table "locations", force: true do |t|
    t.string   "country"
    t.string   "state"
    t.float    "longitude"
    t.float    "latitude"
    t.datetime "created_at"
    t.datetime "updated_at"
  end

  create_table "metrics", force: true do |t|
    t.string   "name"
    t.datetime "created_at"
    t.datetime "updated_at"
  end

end
