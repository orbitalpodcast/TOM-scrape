# TOM-scrape
This is example code for scraping a podcast on Squarespace and uploading the data to [TOM-site](https://github.com/orbitalpodcast/TOM-site).

### Key concepts included in this example code:

- HTTP GET requests using Requests library
- Parsing HTML with Beautiful Soup
- Reading and writing data to a file using JSON
- Reading and writing binary data to disk
- Creating HTTP POST and PATCH requests
- Formatting data in those requests to interface with Rails' ActiveRecord
- Interpreting errors from failed POST requests

### The code

**tom-scrape.py** is pretty universal. Different SS themes might mess with it, and of course your content will be completely different than mine, but it should be a pretty full-fleshed example. Please feel free to use this code, but please do change the user agent.

**tom-upload.py** is specific to the API of my website, but it's a great example of how to upload binary files to a Rails application! The key here is to not include content-type in the HTTP header ([HUGE thanks to Dakota Lillie for this insight!](https://itnext.io/uploading-files-to-your-rails-api-6b293a4a5c90)).

Please see my [other repo](https://github.com/orbitalpodcast/TOM-site) for the full server code that this script interacts with, but the basics are as follows:

```ruby
  # POST /episodes
  # POST /episodes.json
  def create
    @episode = Episode.new(episode_params.except(:images))
    respond_to do |format|
      if @episode.save
        format.json { render :show, status: :created, location: @episode }
      else
        format.json { render json: {errors: @episode.errors}, status: 422, encoding: 'application/json' }
      end
    end
  end

  # PATCH/PUT /episodes/1
  # PATCH/PUT /episodes/1.json
  def update
    respond_to do |format|
      if @episode.update( episode_params.except(:images))
        update_attachments
        format.json { render :show, status: :accepted, location: @episode }
      else
        format.json { render json: {errors: @episode.errors}, status: 422, encoding: 'application/json' }
      end
    end
  end  

  # PATCH/PUT /upload_audio/1
  def upload_audio
    unless @episode = Episode.find_by(number: params[:number])
      render inline: '{"errors":{"number":"non-existant episode number."}}', status: 422, encoding: 'application/json' and return
    end
    file = params[:file]
    @episode.audio.attach(file)
  end

  # DELETE /episodes/1
  # DELETE /episodes/1.json
  def destroy
    @episode.destroy
    respond_to do |format|
      format.html { redirect_to episodes_url, notice: 'Episode was successfully destroyed.' }
      format.json { head :no_content }
    end
  end
```

