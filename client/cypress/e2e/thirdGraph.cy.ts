describe('Third Graph Selection', () => {
  it('navigates to the graphs page, selects the third graph, and verifies the image', () => {
    cy.visit('http://localhost:8080');

    // Button
    cy.get('.btn-danger')
      .should('be.visible')
      .and('have.text', 'Explore Data')
      .click();

    cy.url().should('eq', 'http://localhost:8080/graphs');

    cy.get(':nth-child(5) > :nth-child(1) > .card > .card-text')
      .should('be.visible')
      .and('contain.text', 'Most Popular Items Sold on average');

    cy.get(':nth-child(5) > :nth-child(1) > .card > .card-body > :nth-child(2)')
      .should('be.visible')
      .and('contain.text', 'Select Graph (average per day of the week)')
      .click();

    // display graph page
    cy.url().should('eq', 'http://localhost:8080/display_graph');

    // image is visible
    cy.get('img')
      .should('be.visible');
  });
});
