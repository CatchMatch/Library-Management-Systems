function openPopup(bookId, title, author, description) {
      document.getElementById('popupTitle').textContent = title;
      document.getElementById('popupAuthor').textContent = author;
      document.getElementById('popupDescription').textContent = description;
      document.getElementById('borrowForm').action = `/borrow/${bookId}/`;
      document.getElementById('popup').style.display = 'block';
    }

    function closePopup() {
      document.getElementById('popup').style.display = 'none';
    }

    document.getElementById('searchInput').addEventListener('input', function () {
      const filter = this.value.toLowerCase();
      const books = document.querySelectorAll('.book');
      books.forEach(book => {
        const title = book.querySelector('.book-title').textContent.toLowerCase();
        const author = book.querySelector('.book-author').textContent.toLowerCase();
        if (title.includes(filter) || author.includes(filter)) {
          book.style.display = '';
        } else {
          book.style.display = 'none';
        }
      });
    });