describe('template spec', () => {
  it('passes', () => {
    const url = 'https://mail.tm';
    cy.visit(url + '/ru/');
    cy.wait(500);

    cy.get('button[title="Аккаунт"]').click();
    cy.wait(550);

    cy.get('button[role="menuitem"]').then(elems => {
      elems[1].click();
    });
    cy.wait(450);

    cy.get('input[name="address"]').type("artem159@freesourcecodes.com");
    cy.wait(300);
    cy.get('input[name="password"]').type("qBe37aar");
    cy.wait(400);
    cy.get('button[class="w-full inline-flex justify-center border border-transparent rounded-md bg-indigo-600 px-4 py-2 text-base font-medium leading-6 text-white shadow-sm transition focus:border-indigo-700 dark:bg-indigo-700 hover:bg-indigo-500 sm:text-sm sm:leading-5 focus:outline-none focus:ring-indigo dark:hover:bg-indigo-800"]')
      .click();
    cy.wait(600);

    const mails = [];
    cy.get('a[class="group block transition hover:bg-gray-50 focus:outline-none dark:focus:bg-gray-900/50 dark:hover:bg-gray-900/50"]')
      .each((elem, index) => {
        cy.log(index);
        cy.wait(500);

        cy.get('a[class="group block transition hover:bg-gray-50 focus:outline-none dark:focus:bg-gray-900/50 dark:hover:bg-gray-900/50"]')
          .eq(index).as('mail');
        cy.get('@mail').click();

        cy.get('h2[class="text-2xl font-bold leading-7 text-gray-900 sm:truncate dark:text-gray-300"]', 
          { timeout: 10000 }).should('exist');
        cy.wait(300);
        
        let header, name, email, time, text;
        cy.get('h2[class="text-2xl font-bold leading-7 text-gray-900 sm:truncate dark:text-gray-300"]')
          .then(elem => {
            header = elem.text();
          });
        cy.get('div[class="text-lg font-medium leading-6 text-indigo-600"]')
          .then(elem => {
            name = elem.text();
          });
        cy.get('span[class="text-sm font-normal leading-5 text-gray-700"]')
          .then(elem => {
            email = elem.text();
          });
        cy.get('time').then(elem => {time = elem.text();});
        cy.get('iframe')
          .its('0.contentDocument.body')
          .should('not.be.empty')
          .then(cy.wrap)
          .within(() => {
            cy.get('div').then(elem => text = elem.text());
          });
        
        cy.then(() => {
          cy.log(`${header} ${name} ${email} ${time}`);
          cy.log(text);

          mails.push({
            'title': header,
            'author': name,
            'email': email,
            'date': time,
            'text': text
          });
          cy.log(mails);
        });
        cy.go('back');
        cy.wait(600);
      }); 
    cy.then(() => {
      cy.writeFile('mails_by_cypress.json', mails);
    });     
  })
})