describe('Test Front Page of Application', () => {
  it('loads the main page correctly', () => {
    cy.visit('http://localhost:8080');

    // button is visible
    cy.get('.btn-danger')
      .should('be.visible')
      .and('have.text', 'Explore Data');

    // image is visible
    cy.get('.img-fluid')
      .should('be.visible')
      .and('have.attr', 'src')
      .should('not.be.empty');
  });

  it('navigates to the graphs page when "Explore Data" is clicked', () => {
    cy.visit('http://localhost:8080');
    cy.get('.btn-danger').click();
    cy.url().should('eq', 'http://localhost:8080/graphs');
  });
});
