export default {
    template: `<div >
    <div class="container">
    <hr>
    <h1>Create Album</h1>
    <hr>
    <form >
  <div class="form-group col-md-6">
    <label for="exampleFormControlFile1">Album Display picture :</label>
    <input type="file" class="form-control-file" id="albumpicture">
  </div>
  <hr>
  <div class="form-row">
    <div class="form-group col-md-6">
      <label for="inputEmail4">ALBUM NAME:</label>
      <input type="email" class="form-control" id="songname" placeholder="album name">
    </div>
    <div class="form-group col-md-6">
      <label for="inputPassword4">ARTIST:</label>
      <input type="password" class="form-control" id="genre" placeholder="Artist">
    </div>
    <div class="form-group col-md-6">
      <label for="inputPassword4">LANGUAGE:</label>
      <input type="password" class="form-control" id="genre" placeholder="language">
    </div>
  </div>
  </div>
  <br>
  <div class="container">
  <button type="button" class="btn btn-primary btn-lg btn-block">UPLOAD</button>
  </div>
</form>
</div>
</div>`,
  }