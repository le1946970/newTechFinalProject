describe('Graph Selection with DatePicker', () => {
  it('navigates to the graphs page and selects a graph', () => {
    cy.visit('http://localhost:8080');

    cy.get('.btn-danger')
      .should('be.visible')
      .and('have.text', 'Explore Data')
      .click();

    //navigation to graph page
    cy.url().should('eq', 'http://localhost:8080/graphs');

    cy.get('.form-control')
      .should('be.visible')
      .type('2024-12-06');

    cy.get('body').click();

    // select graph button
    cy.get(':nth-child(4) > :nth-child(1) > .card > .card-body > .btn')
      .should('be.visible')
      .and('have.text', 'Select Graph')
      .click();

    //display_graph page
    cy.url().should('eq', 'http://localhost:8080/display_graph');

    // graph image
    cy.get('img')
      .should('be.visible')
      .and('have.attr', 'src')
      .should('not.be.empty');
  });
});
